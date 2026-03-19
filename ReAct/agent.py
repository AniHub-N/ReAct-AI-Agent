from parser import ActionParser
from tools import ToolRegistry


class ReactAgent:

    def __init__(self, llm):
        self.llm = llm
        self.parser = ActionParser()
        self.tools = ToolRegistry()
        self.history = []
        self.fail_count = 0  #  NEW: track failures

    #  SELF-CRITIQUE (LEVEL 3)
    def critic(self, answer):

        critique_prompt = f"""
Evaluate this answer:

{answer}

If correct → output ONLY: OK
If incorrect → output ONLY the corrected answer

NO explanations.
"""

        response = self.llm(critique_prompt).strip()

        #  Extract only final answer if not OK
        if response == "OK":
            return "OK"

        # Try to extract improved answer
        if "Improved answer:" in response:
            return response.split("Improved answer:")[-1].strip()

        # fallback
        return response.split("\n")[-1].strip()

    def build_prompt(self):

        context = "\n".join(self.history[-6:])  #  sliding window

        return f"""
You are a STRICT ReAct agent.

YOU MUST FOLLOW RULES EXACTLY:

1. Use ONLY these tools:
- search
- calculator

2. NEVER combine Action and input
3. NEVER write Action like: search "query"
4. ALWAYS use:
Action: search
Action Input: query

5. Action Input must NEVER be empty

6. After Action → WAIT for Observation

7. Do NOT guess answers without observation

8. Do NOT give Final Answer in same step as Action

FORMAT:

Thought:
Action:
Action Input:

OR

Thought:
Final Answer:

{context}
"""

    #  MAIN LOOP
    def run(self, question):

        self.history = [f"Question: {question}"]
        self.fail_count = 0  # reset per run

        for step in range(10):

            prompt = self.build_prompt()
            response = self.llm(prompt)

            print("\nLLM OUTPUT:\n", response)

            #  FAILURE DETECTION: refusal
            if "cannot provide" in response.lower():
                self.fail_count += 1
            else:
                self.fail_count = 0

            #  STOP if repeated failure
            if self.fail_count >= 3:
                return "Agent stopped: repeated failure / refusal."

            parsed = self.parser.parse(response)

            #  FINAL ANSWER
            if parsed["type"] == "final":

                answer = parsed["answer"].strip()
                full_context = "\n".join(self.history)

                #  Must have used tools first
                if "Observation:" not in full_context:
                    self.history.append(response)
                    self.history.append(
                        "Observation: You must use a tool and get an Observation before answering."
                    )
                    self.history.append("Continue step-by-step. Do not skip steps.")
                    continue

                #  Reject empty / bad answers
                if (
                        not answer
                        or answer.lower().startswith("note")
                        or "i cannot" in answer.lower()
                        or "waiting" in answer.lower()
                    ):
                    self.history.append(response)
                    self.history.append(
                        "Observation: INVALID FINAL ANSWER. Provide a clear, direct answer only."
                    )
                    self.history.append("Continue step-by-step. Do not skip steps.")
                    continue

                #  SELF-CRITIQUE
                critique = self.critic(answer)

                #  CASE 1: empty or garbage → ignore critic
                if not critique or critique.strip() == "":
                    return answer

                #  CASE 2: critic says OK → trust original
                if critique == "OK":
                    return answer

                #  CASE 3: validate improved answer (VERY IMPORTANT)
                clean = critique.strip().lower()

                if (
                    "i'm ready" in clean
                    or "what's the question" in clean
                    or "cannot" in clean
                    or len(clean) < 5
                ):
                    return answer  #  reject bad critic output

                #  only now accept critic
                print("\nCRITIC IMPROVED ANSWER:\n", critique)
                return critique

            #  ACTION HANDLING
            elif parsed["type"] == "action":

                #  Block Action + Final Answer together
                if "Final Answer:" in response:
                    self.history.append(response)
                    self.history.append(
                        "Observation: INVALID. Action and Final Answer cannot be in same step."
                    )
                    self.history.append("Continue step-by-step. Do not skip steps.")
                    continue

                tool_name = parsed["action"].lower().strip()
                tool_input = parsed["input"].strip().strip('"')

                #  Invalid tool
                if tool_name not in self.tools.tools:
                    self.history.append(response)
                    self.history.append(
                        f"Observation: INVALID TOOL '{tool_name}'. Use only: search, calculator."
                    )
                    self.history.append("Continue step-by-step. Do not skip steps.")
                    continue

                #  Invalid input
                if not tool_input or tool_input.lower() == "none":
                    self.history.append(response)
                    self.history.append(
                        "Observation: INVALID INPUT. Action Input cannot be empty."
                    )
                    self.history.append("Continue step-by-step. Do not skip steps.")
                    continue

                #  Execute tool
                observation = self.tools.execute(tool_name, tool_input)

                #  Compress observation
                observation = observation[:200]

                #  NEW: Detect unreliable / conflicting data
                if (
                        not observation
                        or "no relevant" in observation.lower()
                        or "unknown" in observation.lower()
                    ):
                    self.history.append(response)
                    self.history.append(
                        "Observation: Data may be unreliable or conflicting. Try a different search query."
                    )
                    self.history.append("Continue step-by-step. Do not skip steps.")
                    continue

                #  INVALID FORMAT
                elif parsed["type"] == "invalid":
    
                    self.history.append(response)
                    self.history.append(
                        "Observation: Invalid format. "
                        "You must follow:\nThought → Action → Action Input OR Final Answer"
                    )
                    self.history.append("Continue step-by-step. Do not skip steps.")

        return "Unable to find a reliable answer after multiple attempts."
import re


class ActionParser:

    def parse(self, text):

        # Final answer
        if "Final Answer:" in text:
            answer = text.split("Final Answer:")[-1].strip()
            return {"type": "final", "answer": answer}

        # Try normal format
        action_match = re.search(r"Action:\s*(\w+)", text)
        input_match = re.search(r"Action Input:\s*(.*)", text)

        #  NEW: handle inline input like:
        # Action: search "CEO of OpenAI"
        inline_match = re.search(r"Action:\s*(\w+)\s+\"(.+?)\"", text)

        if inline_match:
            return {
                "type": "action",
                "action": inline_match.group(1),
                "input": inline_match.group(2)
            }

        if action_match:
            action = action_match.group(1)

            if input_match:
                action_input = input_match.group(1).strip()
            else:
                action_input = ""

            return {
                "type": "action",
                "action": action,
                "input": action_input
            }

        return {"type": "invalid", "raw": text}
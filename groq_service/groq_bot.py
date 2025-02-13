import os
import requests
from groq import Groq


class GroqBot:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
        self.reset_chat()

    def reset_chat(self):
        self.messages = [
            {"role": "system",
             "content": """
             You are an interactive assistant that collects report details from the user step by step. User not able find a report based on his query.
             Ask relevant follow-up questions to gather complete information before summarizing the report requirements. 
             Ask few question with some options so that user can select one/more options from them itself.
             Do not ask more than 5 questions. Make sure you collect the user email id. 
            """
            }
        ]

    def get_groq_response(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            model=os.environ.get("GROQ_MODEL"),  # Replace with actual model name
            messages=self.messages
        )
        reply = response.choices[0].message.content.strip()
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def collect_report_details(self):
        self.reset_chat()
        initial_question = "What details do you want to provide about the report?"
        next_question = initial_question
        question_count = 0

        while question_count < 5:
            user_input = input(next_question + " ")
            if user_input.lower() in ["exit", "quit", "done"]:
                break

            self.messages.append({"role": "user", "content": user_input})
            response = self.get_groq_response(f"User provided: {user_input}. Ask a relevant follow-up question.")

            if response.lower() in ["end", "no more questions"]:
                break

            next_question = response
            question_count += 1

    def confirm_and_summarize(self):
        summary_request = "Summarize the provided report details."
        summary = self.get_groq_response(summary_request)
        print("AI Summary:", summary)
        self.send_to_slack(summary)

    def send_to_slack(self, summary):
        if self.slack_webhook_url:
            payload = {"text": f"Report Summary:\n{summary}"}
            requests.post(self.slack_webhook_url, json=payload)
            print("Summary sent to Slack.")
        else:
            print("Slack webhook URL not configured.")
from dataclasses import dataclass
from typing import List, Tuple
import re

@dataclass
class Email:
    sender: str
    subject: str
    body: str

# Dummy email data
DUMMY_EMAILS: List[Email] = [
    Email(sender="Sumana <sumana@example.com>", subject="dinner tonight", body="Want to do dinner at home?"),
    Email(sender="Garry Tan <garry@yc.com>", subject="reschedule", body="Need to reschedule our meeting."),
    Email(sender="Alex Chen <alex@example.com>", subject="advice on fundraising", body="Can I get your thoughts on fundraising?"),
    Email(sender="Gustaf Alstr\xf6mer <gustaf@yc.com>", subject="founder intro?", body="Have a founder you should meet."),
    Email(sender="Maya Rodriguez <maya@example.com>", subject="Technical co-founder?", body="Know anyone interested in joining as CTO?"),
    Email(sender="HackerNews Digest <news@hn.com>", subject="Top Stories: New Programming Languages", body="Lot's happening in tech this week."),
    Email(sender="TechCrunch Weekly <newsletter@techcrunch.com>", subject="This Week in Tech: AI Developments and Market Trends", body="In this week's roundup we cover..."),
    Email(sender="The Verge Updates <updates@theverge.com>", subject="Latest Product Launches and Industry News", body="Today in tech..."),
    Email(sender="DevOps Pro Team <sales@devopspro.com>", subject="Security Solutions for Growing Companies", body="We have tools that will transform your workflow."),
    Email(sender="DataAnalytics Plus <pricing@dap.com>", subject="Special Pricing on Data Analytics Tools", body="Exclusive offer inside."),
    Email(sender="Sarah from SaaS Solutions <sarah@saassolutions.com>", subject="Exclusive Offer for New Customers", body="Get 20% off if you sign up now"),
    Email(sender="Mark at Enterprise Tools <mark@enterprisetools.com>", subject="Transform Your Workflow with Our Platform", body="Our platform will increase productivity"),
]

class EmailAssistant:
    """Simple rule-based assistant using Pete's labeling logic."""

    def process_email(self, email: Email) -> List[Tuple[str, ...]]:
        sender = email.sender.lower()
        subject = email.subject.lower()
        body = email.body.lower()
        actions: List[Tuple[str, ...]] = []

        if "sumana" in sender:
            actions.append(("labelEmail", "Personal", "red", "0"))
            actions.append(("draftReply", "sounds good -Pete"))
        elif "garry" in sender:
            actions.append(("labelEmail", "YC", "orange", "1"))
            actions.append(("draftReply", "will do thx -Pete"))
        elif "@yc.com" in sender:
            actions.append(("labelEmail", "YC", "orange", "2"))
            actions.append(("draftReply", "thanks will follow up -Pete"))
        elif any(name in sender for name in ["alex", "maya", "gustaf"]):
            actions.append(("labelEmail", "Founders", "blue", "2"))
            actions.append(("draftReply", "happy to chat -Pete"))
        elif any(word in subject for word in ["digest", "weekly", "updates"]):
            actions.append(("labelEmail", "Tech", "gray", "3"))
        elif any(word in body for word in ["exclusive", "pricing", "offer", "workflow"]):
            actions.append(("archiveEmail",))
        else:
            actions.append(("labelEmail", "General", "gray", "3"))
        return actions


def main() -> None:
    assistant = EmailAssistant()
    for email in DUMMY_EMAILS:
        print(f"---\nFrom: {email.sender}\nSubject: {email.subject}")
        actions = assistant.process_email(email)
        for act in actions:
            if act[0] == "labelEmail":
                _, label, color, priority = act
                print(f"labelEmail(label={label}, color={color}, priority={priority})")
            elif act[0] == "draftReply":
                _, body = act
                print(f"draftReply(body={body})")
            elif act[0] == "archiveEmail":
                print("archiveEmail()")

if __name__ == "__main__":
    main()

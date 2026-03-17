import os
from atlassian import Jira
from dotenv import load_dotenv

# 加載 Jira 專屬環境變數
env_path = "/Users/linjingying/Desktop/vibe coding/JennyCargo_System/.jira_env"
with open(env_path, "r") as f:
    for line in f:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            os.environ[key] = value

jira_url = os.getenv("JIRA_URL")
jira_user = os.getenv("JIRA_USER")
jira_token = os.getenv("JIRA_API_TOKEN")

jira = Jira(
    url=jira_url,
    username=jira_user,
    password=jira_token,
    cloud=True
)

def reply_to_issue(issue_key, comment_text):
    print(f"🚀 正在為 {issue_key} 新增留言...")
    try:
        jira.issue_add_comment(issue_key, comment_text)
        print(f"✅ 成功！已在 {issue_key} 上回覆。")
    except Exception as e:
        print(f"❌ 發生錯誤：{str(e)}")

if __name__ == "__main__":
    # 這裡可以根據需要手動調用，或由 Agent 自動調用
    import sys
    if len(sys.argv) > 2:
        reply_to_issue(sys.argv[1], sys.argv[2])
    else:
        # 預設查詢測試
        issue = jira.issue("EPB-47741")
        print(f"測試成功！抓取到任務標題：{issue['fields']['summary']}")

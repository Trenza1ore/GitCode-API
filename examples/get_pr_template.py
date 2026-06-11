from gitcode_api import GitCode

client = GitCode()

# 获取仓库以及上游仓库的PR模版
templates = client.pulls.list_templates(owner="SushiNinja", repo="agent-core-contrib")

# 选取特定模版
english_template = [t for t in templates if t.path.endswith(".en.md")][0]
template_text = client.pulls.get_template(
    path=english_template.path, owner=english_template.template_owner, repo=english_template.template_repo
)
print(template_text)

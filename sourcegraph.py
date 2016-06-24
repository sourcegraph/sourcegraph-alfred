 # encoding: utf-8

import sys

from workflow import Workflow, ICON_WEB, web
from urllib import quote
 


icon_mapping = {
    "Java": "images/icons/java.png",
    "C": "images/icons/c-original.png",
    "Go": "images/icons/go-original.png",
    "C#": "images/icons/csharp-original.png",
    "Python": "images/icons/python-original.png"
}

def get_posts(query):
    url = "https://sourcegraph.com/.api/global-search?Query=%s&Limit=15" % query.replace(' ' , '+')

    request = web.get(url)

    # throw an error if request failed
    # Workflow will catch this and show it to the user
    request.raise_for_status()

    # Parse the JSON returned by pinboard and extract the posts
    result = request.json()
    posts = result['Defs']
    return posts

def main(wf):

    if wf.args and len(wf.args) > 1:
        searchtype = wf.args[0]
        query = wf.args[1]

        searchtype = "info" if searchtype == 'i' else "def"

        posts = get_posts(query)

        wf.clear_data()

        if not posts:
            wf.add_item(title="No results found for \"%s\"" % query,
                        subtitle = "",
                        valid=False,
                        icon='images/sourcegraph-mark.png')
            wf.send_feedback()
            return
        for post in posts:
            try:
                arg = post['Repo']

                # for packages, the entire file path does not need to be generated
                if post['File'] != "" and post['File'] != "." and post['Kind'] != "package":
                    arg += "/-/%s/%s/%s/-/%s" % (searchtype, post['UnitType'], post['Unit'], post['Path'])

                icon = "images/icons/doc-code.png"
                if post['FmtStrings']['Language'] in icon_mapping:
                    icon = icon_mapping[post['FmtStrings']['Language']]
                title = post['FmtStrings']['Name']['ScopeQualified']
                subtitle = "from %s" % post['FmtStrings']['Name']['LanguageWideQualified']
                wf.add_item(title=title,
                            subtitle=subtitle,
                            arg= arg,
                            valid=True,
                            icon=icon)
            except Exception as e:
                sys.stderr.write(str(e))
        # Send the results to Alfred as XML
        wf.send_feedback()
        
if __name__ == u"__main__":

    update_settings = {
        'github_slug': 'sourcegraph/sourcegraph-alfred',
        'frequency': 1
    }

    wf = Workflow(update_settings=update_settings)
    if wf.update_available:
        wf.start_update()
    sys.exit(wf.run(main))

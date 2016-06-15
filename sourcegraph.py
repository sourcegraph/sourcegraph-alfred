 # encoding: utf-8

import sys
from workflow import Workflow, ICON_WEB, web
from urllib import quote

def main(wf):

    if wf.args and len(wf.args) > 1:
        searchtype = wf.args[0]
        query = wf.args[1]

        searchtype = "info" if searchtype == 'i' else "def"

        url = "https://sourcegraph.com/.api/global-search?Query=%s&Limit=10" % query.replace(' ' , '+')

        request = web.get(url)

        # throw an error if request failed
        # Workflow will catch this and show it to the user
        request.raise_for_status()

        # Parse the JSON returned by pinboard and extract the posts
        result = request.json()
        posts = result['Defs']

        wf.clear_data()

        if not posts:
            wf.add_item(title="No results found for \"%s\"" % query,
                        subtitle = "",
                        valid=False,
                        icon='sourcegraph-mark.png')
            wf.send_feedback()
            return
        for post in posts:
            try:
                title = post['FmtStrings']['Name']['ScopeQualified']
                subtitle = "from %s" % post['FmtStrings']['Name']['LanguageWideQualified']
                wf.add_item(title=title,
                            subtitle=subtitle,
                            arg= "%s/-/%s/%s/%s/-/%s" % (post['Repo'], searchtype, post['UnitType'], post['Unit'], post['Path']),
                            valid=True,
                            icon='doc-code.png')
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

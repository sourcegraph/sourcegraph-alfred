 # encoding: utf-8

import sys
from workflow import Workflow, ICON_WEB, web
from urllib import quote

def main(wf):

    if wf.args and len(wf.args) > 1:
        searchtype = wf.args[0]
        query = wf.args[1]


        searchtype = "info" if searchtype == 'i' else "def"

        url = 'https://sourcegraph.com/.api/global-search?Query='+query.replace(' ' , '+')+'&Limit=10'
        request = web.get(url)

        # throw an error if request failed
        # Workflow will catch this and show it to the user
        request.raise_for_status()

        # Parse the JSON returned by pinboard and extract the posts
        result = request.json()
        posts = result['Defs']



        # Loop through the returned posts and add an item for each to

        # the list of results for Alfred

        item_count = 0
        if posts:
            for post in posts:
                    #print("https://sourcegraph.com/"+post['Repo']+'/-/info/'+post['UnitType']+'/'+post['Unit']+'/-/'+post['Path'])
                try:
                    item_count += 1
                    wf.add_item(title=post['Unit'],
                                subtitle=post['FmtStrings']['Language'] + " " + post['Repo'],
                                arg= post['Repo']+'/-/'+searchtype+'/'+post['UnitType']+'/'+post['Unit']+'/-/'+post['Path'],
                                valid=True,
                                icon='doc-code.png')
                except Exception as e:
                    continue

        if item_count == 0:
            wf.add_item(title= 'No results found for "'  + query + '" ',
                        subtitle = "",
                        valid=True,
                        icon='sourcegraph-mark.png')



        # Send the results to Alfred as XML
        wf.send_feedback()

    else:
        query = None
        wf.add_item(title="Fetching Results...",
                        subtitle="",
                        arg= "",
                        valid=False ,
                        icon='sourcegraph-mark.png')


        wf.send_feedback()



if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))

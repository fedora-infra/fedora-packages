<div id="${id}">
    % for entry in feed.iterentries(d=d, limit=limit):
        <div class="entry">
            <div id="${entry['uid']}">
                <div id="${entry['uid']}_person" class="person-info">
                         <img src="${entry.author_detail.get('hackergotchi', 'http://planet.fedoraproject.org/images/heads/default.png')}" height="40" />
                    <a title="${entry.author_detail.name}'s blog" href="${entry.author_detail.href}"> 
                         ${entry.author_detail.name}
                    </a>
                </div>
                <div class="post">
                    <div class="post-header">
                        <h4 class="post-title">
                            <a href="${entry.link}" target="_blank">${entry.title}</a></span>
                        </h4>
                    </div>
                    <div class="post-contents" id="${entry['uid']}_text">
                        ${entry.content[0].value}
                    </div>
                    <div class="post-footer">
                    </div>
                    <b class="vt lt">&nbsp;</b>
                    <b class="vt rt">&nbsp;</b>
                    <b class="hz to">&nbsp;</b>
                    <b class="hz bo">&nbsp;</b>
                    <b class="cr tl">&nbsp;</b>
                    <b class="cr tr">&nbsp;</b>
                    <b class="cr bl">&nbsp;</b>
                    <b class="cr br">&nbsp;</b>
                </div>
            </div>
        </div>
        <script>

            hackergochi = $("#${entry['uid']}_text img:first");
            if (hackergochi) {
                $("#${entry['uid']}_person img:first").remove();
                $("#${entry['uid']}_person").prepend($("#${entry['uid']}_text img:first"));
            }

        </script>
    % endfor
</div>

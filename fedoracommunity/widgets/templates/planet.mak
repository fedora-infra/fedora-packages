<div id="${id}" class="list">
    % for entry in entries[:limit]:
        <div class="entry">
            <div id="${entry['uid']}">
                <div id="${entry['uid']}_person" class="person-info">
                         <img src="${entry.author_detail.get('hackergotchi', 'http://planet.fedoraproject.org/images/heads/default.png')}" height="40" />
                    <a title="${entry.author_detail.name}'s blog" href="${entry.author_detail.href}" target="_blank">
                         ${entry.author_detail.name}
                    </a>
                </div>
                <div class="post">
                    <div class="post-header">
                        <h4 class="post-title">
                            <span><a href="${entry.link}">${entry.title}</a></span>
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

            function img_error(source) {
                source.src = "http://planet.fedoraproject.org/images/heads/default.png";
                source.onerror = "";
                return true;
            }

            hackergochi = $("#${entry['uid']}_text img:first");
            if (hackergochi) {
                hackergochi.attr('onerror', 'img_error(this)');
                $("#${entry['uid']}_person img:first").remove();
                $("#${entry['uid']}_person").prepend(hackergochi);
            }

            $("#${entry['uid']}_text").expander({
                slicePoint: 300,
                widow: 1,
                userCollapse: true,
                expandText: '<strong>Show more</strong> <img src="/images/arrow_down.png">',
                userCollapseText: '<strong>Hide full post content</strong> <img src="/images/arrow_up.png">',
            });

        </script>
    % endfor
<div align="right"><a href="http://planet.fedoraproject.org">View more ></a></div>
</div>

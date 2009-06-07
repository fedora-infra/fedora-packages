% if entries:
  <h3>Latest Blog Posts</h3>
  <div id="${id}" class="simple-border-list list">
    <table>
      % for entry in entries[:limit]:
        <tr>
          <td class="blog-post">
            <b><a href="${entry.link}">${entry.title}</a></b>
            <br/>
            <div class="post-contents" id="${entry['uid']}_text">
              ${entry.summary}
            </div>
            <div class="last-modified">
              Posted ${entry['last_modified']}
            </div>
          </td>
          <script type="text/javascript">
              $("#${entry['uid']}_text").expander({
                  slicePoint: 300,
                  widow: 1,
                  userCollapse: true,
                  expandText: '<strong>Show more</strong> <img src="${tmpl_context.get_url('/images/arrow_down.png')}">',
                  userCollapseText: '<strong>Hide full post content</strong> <img src="${tmpl_context.get_url('/images/arrow_up.png')}">',
              });

          </script>
        </tr>
      % endfor
    </table>
    % if username:
        <div align="right">
          <a href="${url}">View ${username}'s blog &gt;</a>
        </div>
    % endif
  </div>
% endif

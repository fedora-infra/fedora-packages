<div id="${id}" class="simple-list list">
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
        <script>
            $("#${entry['uid']}_text").expander({
                slicePoint: 300,
                widow: 1,
                userCollapse: true,
                expandText: '<strong>Show more</strong> <img src="/images/arrow_down.png">',
                userCollapseText: '<strong>Hide full post content</strong> <img src="/images/arrow_up.png">',
            });

        </script>
      </tr>
    % endfor
  </table>
</div>

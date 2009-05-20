<div id="${id}">
<div class="overlay"><div class="message"></div></div>

<script>
var package_name = "${package}";
var uid = "${id}";
</script>

<h3>Release</h3>
${c.releases(options=releases, value=release)}

% if latest_srpm:
    <div class="list simple-list">
    <h3>Source</h3>
    <table>
      <tr>
        <th>Latest Spec File</th>
        <td><a href="${latest_spec}">${latest_srpm['name']}.spec</a></td>
      </tr>
      <tr>
        <th>Latest SRPM</th>
        <td><a href="${latest_srpm['url']}">${latest_srpm['nvr']}</a> <span class="filesize">(${latest_srpm['size']})</span></td>
      </tr>
    </table>
    </div>

    <div class="list header-list">
    <h3>Binaries</h3>
    <table>
      <tr>
        <th>Architecture</th>
        <th>Downloads</th>
      </tr>
        % for arch in [arch for arch in architectures if arches[arch]]:
          <tr>
            <td>${arch}</td>
            <td>
              % for download in sorted(arches[arch]):
                <a href="${download['url']}">${download['nvr']}</a> <span class="filesize">(${download['size']})</span><br/>
              % endfor
            </td>
          </tr>
      % endfor
    </table>
    </div>
% else:
    <center>No downloads found</center>
% endif
</div>

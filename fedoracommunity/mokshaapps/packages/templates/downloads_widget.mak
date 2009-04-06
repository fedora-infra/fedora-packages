<script>
var package_name = "${package}";
</script>

<h3>Release</h3>
${c.releases(options=releases, value=release)}

% if latest_srpm:
    <h3>Source</h3>
    <table>
      <tr>
        <td align="right"><b>Latest Spec File</b></td>
        <td><a href="${latest_spec}">${latest_srpm['name']}.spec</a></td>
      </tr>
      <tr>
        <td align="right"><b>Latest SRPM</b></td>
        <td><a href="${latest_srpm['url']}">${latest_srpm['nvr']}</a> <span class="filesize">(${latest_srpm['size']})</span></td>
      </tr>
    </table>
    <h3>Binaries</h3>
    <table>
      <tr>
        <th>Architecture</th>
        <th>Downloads</th>
      </tr>
      % for arch in arches:
          <tr>
            <td>${arch}</td>
            <td>
              % for download in arches[arch]:
                <a href="${download['url']}">${download['nvr']}</a> <span class="filesize">(${download['size']})</span><br/>
              % endfor
            </td>
          </tr>
      % endfor
    </table>

% else:
    <center>No downloads found</center>
% endif

<h3>Source for Active Releases</h3>
<table>
  <tr>
    <th>Release</th>
    <th>Released Version</th>
    <th>Newest SRPM</th>
  </tr>
  % for source in sources:
    <tr>
      <td>${source['release']}</td>
      <td>${source['released_version']}</td>
      <td><a href="${source['url']}">${source['nvr']}</a> <span class="filesize">(${source['size']} SRPM file)</span></td>
    </tr>
  % endfor
</table>

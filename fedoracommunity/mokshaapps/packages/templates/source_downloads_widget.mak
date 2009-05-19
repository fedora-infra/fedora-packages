
<div class="list header-list">
<h3>Source for Active Releases</h3>
<table>
  <tr>
    <th>Release</th>
    <th>Released Version</th>
    <th>Newest SRPM</th>
  </tr>
  % for source in sources:
    <tr>
      <td><strong>${source['release']}</strong></td>
      <td>${source['released_version']}</td>
      <td><a href="${source['url']}">${source['nvr']}</a><br /><em class="note">${source['size']} SRPM file</em></td>
    </tr>
  % endfor
</table>
</div>

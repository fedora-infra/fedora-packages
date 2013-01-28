<%def name="render_diffstat(diffstat)">
<table class="diffstat">
<thead><tr><th>File</th><th>Changes</th></tr></thead>
<% diffstat_split = diffstat.strip().split('\n') %>
% for line in diffstat_split[:-1]:
	<% split = line.split('|') %>
	<tr><td>${split[0]}</td><td>${split[1]}</td></tr>
% endfor
<tr><td colspan="2" class="split">${diffstat_split[-1]}</td></tr>
</table>
</%def>


<%def name="render_diffstat(diffstat)">
<table class="diffstat">
<thead><tr><td><b>File</b></td><td><b>Changes</b></td></tr></thead>
<% diffstat_split = diffstat.strip().split('\n') %>
% for line in diffstat_split[:-1]:
	<% split = line.split('|') %>
	<tr><td>${split[0]}</td><td>${split[1]}</td></tr>
% endfor
<tr><td colspan="2"><b>${diffstat_split[-1]}</b></td></tr>
</table>
</%def>


<script type="text/javascript">
function on_change(self) {
	$('#patches').load('/_w/package.sources.patches #patches', {
		'package_name': '${w.package}',
		'branch': self.value
		});
}
</script>

${w.children[0].display(on_change='on_change', package=w.package)}

<div id="patches" class="patches">
% if w.patches:
<%namespace file="diffstat.mak" import="render_diffstat"/>

<a class="frame_link" href="#" onclick="return toggle_diffstat()">Show summary of all patches</a>
<div id="diffstat" style="display:none">
% if w.diffstat:
	${render_diffstat(w.diffstat)}
% endif
</div>
<table>
% for patch in sorted(w.patches):
    <tr id="${patch}">
        <td><a href="#" onclick="return toggle_patch('${patch}');">${patch}</a></td>
        <td>Added ${w.patches[patch][0]} ago</td>
        <td>(${w.patches[patch][1]})</td>
    </tr>
% endfor
</table>

% else:
	No patches found
% endif # if w.patches

<script type="text/javascript">
function toggle_patch(patch) {
	var tr = $('#' + patch.replace(/\./g, '\\.'));

	/* If we're already showing the patch, hide it */
	if ( tr.next().attr('id') == 'patch' ) {
		tr.next().remove();
		tr.removeClass('active-patch');
		return false;
	}

	tr.addClass('active-patch').after(
	  $('<tr/>', {id: 'patch'}).addClass('patch-content').append(
		  $('<td/>', {colspan: 3}).load('/widgets/package.sources.patch',
			  {package: '${w.package}', patch: patch, branch: $('#release_select').val()})));
	return false;
}


function toggle_diffstat() {
	if ( $('#diffstat').is(":visible") ) {
		$('#diffstat').hide();
		$('#diffstat_link').text('Show summary of all patches');
	} else {
		$('#diffstat').show();
		$('#diffstat_link').text('Hide summary of all patches');
	}
}
</script>
</div>

<script type="text/javascript">
function on_change(self) {
	$('#patches_container').load(moksha.url('/_w/package.sources.patches #patches'), {
		'package_name': '${w.package}',
		'branch': self.value
		});
}
</script>

${w.children[0].display(on_change='on_change', package=w.package)}

<div id="patches_container">
<div id="patches" class="patches">
% if w.patches:
<%namespace file="diffstat.mak" import="render_diffstat"/>

<a class="frame_link" href="#" onclick="return toggle_diffstat()">Show summary of all patches</a>
<div id="diffstat" class="diffstat-all" "style="display:none">
% if w.diffstat:
	${render_diffstat(w.diffstat)}
% endif
</div>
<table>
% for patch in w.patches:
    <% name = patch['name'] %>
    <tr id="${name}" class="patch-name" onclick="return toggle_patch('${name}');">
        <td><a href="#">${name}</a></td>
        <td class="age">Added ${patch['age']} ago <span class="date">(${patch['date']})</span></td>
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
		  $('<td/>', {colspan: 3}).load(
            moksha.url('/_w/package.sources.patch'), {
                package: '${w.package}',
                patch: patch,
                branch: $('#release_select').val()
                })));

	return false;
}


function toggle_diffstat() {
	if ( $('.diffstat-all').is(":visible") ) {
		$('.diffstat-all').hide();
		$('.frame_link').text('Show summary of all patches');
	} else {
		$('.diffstat-all').show();
		$('.frame_link').text('Hide summary of all patches');
	}
}
</script>
</div>
</div>

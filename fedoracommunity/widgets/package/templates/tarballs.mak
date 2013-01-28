<script type="text/javascript">
function on_change(self) {
	$('#tarballs_container').load(moksha.url('/_w/package.sources.tarballs #tarballs'), {
		'package_name': '${w.package}',
		'branch': self.value
		});
}
</script>

${w.children[0].display(on_change='on_change', package=w.package)}

<div id="tarballs_container">
<div id="tarballs">
% if w.upstream_tarball:
<h2>Upstream Tarball</h2>
<a href="${w.upstream_tarball}">${w.upstream_tarball}</a>
% else:
	No upstream tarball found
% endif
<br/>
<br/>
% if w.fedora_tarball:
<h2>Fedora Look-aside Tarball</h2>
<a href="${w.fedora_tarball}">${w.fedora_tarball}</a>
% else:
	No Fedora tarball found
% endif
</div>
</div>

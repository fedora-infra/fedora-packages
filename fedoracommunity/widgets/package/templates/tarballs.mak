<script type="text/javascript">
function on_change(self) {
	$('#tarballs').load('/_w/package.sources.tarballs #tarballs', {
		'package_name': '${w.package}',
		'branch': self.value
		});
}
</script>

${w.children[0].display(on_change='on_change', package=w.package)}

<div id="tarballs">
<h2>Upstream Tarball</h2>
<a href="${w.upstream_tarball}">${w.upstream_tarball}</a>
<br/>
<br/>
<h2>Fedora Look-aside Tarball</h2>
<a href="${w.fedora_tarball}">${w.fedora_tarball}</a>
</div>

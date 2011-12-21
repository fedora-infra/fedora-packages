<%namespace file="diffstat.mak" import="render_diffstat"/>

% if w.changelog:
<table class="changelog">
    % for change in w.changelog:
        <tr>
            <td>
                &#8226; ${change['msg'].split('\n')[0]}
            </td>
            <td class="author">
                ${change['author']}
						</td>
						<td class="age">
								${change['date'].strftime('%d %b %Y')}</a>
            </td>
    % endfor
</table>
% endif

% if w.diffstat:
${render_diffstat(w.diffstat)}
% endif
<div class="patch_raw">
<a href="http://pkgs.fedoraproject.org/gitweb/?p=${w.package}.git;a=blob_plain;hb=HEAD;f=${w.patch}" target="_blank">Link to raw patch</a>
</div>
<br/>
${w.text}


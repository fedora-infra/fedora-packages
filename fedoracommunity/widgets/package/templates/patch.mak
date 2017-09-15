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
<a href="https://src.fedoraproject.org/rpms/${w.package}/tree/${w.patch}" target="_blank">Link to raw patch</a>
</div>
<br/>
${w.text}


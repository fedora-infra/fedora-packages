<%namespace file="diffstat.mak" import="render_diffstat"/>

% if w.changelog:
<b>ChangeLog:</b>
<table>
    % for change in w.changelog:
        <tr>
            <td>
                &#8226; ${change['msg'].split('\n')[0]}
            </td>
            <td>
                ${change['author']}
            </td>
            <td>
                ${change['date'].strftime('%d %b %Y')}
            </td>
    % endfor
</table>
% endif

% if w.diffstat:
<b>Summary of changes in this patch:</b>
${render_diffstat(w.diffstat)}
% endif
<br/>
${w.text}

<div class="patch_footer">
<a href="http://pkgs.fedoraproject.org/gitweb/?p=${w.package}.git;a=blob_plain;hb=HEAD;f=${w.patch}" target="_blank">Link to raw patch</a>
</div>

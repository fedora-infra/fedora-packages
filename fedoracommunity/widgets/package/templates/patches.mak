<table>
% for patch in sorted(w.patches):
    <tr>
        <td>${patch}</td>
        <td>Added ${w.patches[patch][0]} ago</td>
        <td>(${w.patches[patch][1]})</td>
    </tr>
% endfor
</table>

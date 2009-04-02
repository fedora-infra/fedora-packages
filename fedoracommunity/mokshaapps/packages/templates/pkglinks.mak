<div id="${id}">
    <div class="instructions">View this package in other Fedora Infrastructure Systems</div>
    <ul>
      <li><a href="https://admin.fedoraproject.org/updates/${package}"
             target="_blank">
             <img border=0 src="/images/16_bodhi.png" />Updates
          </a>
      </li>
      <li><a href="http://koji.fedoraproject.org/koji/search?terms=${package}&type=package&match=exact" target="_blank" >
              <img border=0 src="/images/16_koji.png" />Builds
          </a>
      </li>
      <li><a href="https://admin.fedoraproject.org/pkgdb/bugs/name/${package}" target="_blank" >
              <img border=0 src="/images/16_bugs.png" />Bugs
          </a>
      </li>
      <li><a href="http://cvs.fedoraproject.org/viewvc/rpms/${package}" target="_blank" >
              <img border=0 src="/images/16_sources.png" />Source
          </a>
      </li>
      <li><a href="https://admin.fedoraproject.org/pkgdb/packages/name/${package}" target="_blank" >
              <img border=0 src="/images/16_pkgdb.png" />Package Info
          </a>
      </li>
    </ul>
</div>
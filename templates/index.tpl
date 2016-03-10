<body>

% if configmode == True:
 Currently in CONFIG mode
% else:
 Currently in NORMAL mode
%end

%if configmode == True:
 <ul>
  % for network in scanlist:
   <li>{{network}}</li>
  % end
 </ul>
%end
</body>

 function shortenFileName(str, maxLength, ellipsisLocationPercentage,placeholder) {
       if(ellipsisLocationPercentage == null || isNaN(ellipsisLocationPercentage) || ellipsisLocationPercentage >= 1 || ellipsisLocationPercentage <= 0){
           ellipsisLocationPercentage = .85;
       }
       if(placeholder == null || placeholder ==""){
           placeholder = "[...]";
       }
       if (str.length > (maxLength-placeholder.length)) {
           var beginning = str.substr(0, (maxLength - placeholder.length)*ellipsisLocationPercentage );
           var end = str.substr(str.length-(maxLength - placeholder.length) * (1-ellipsisLocationPercentage));
           return beginning + placeholder + end;
       }
       return str;
   } 
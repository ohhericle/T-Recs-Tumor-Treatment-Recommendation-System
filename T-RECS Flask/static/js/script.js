$(function(){
  
  item_height=$(".item").outerHeight(true);
  height=(item_height+2)*($(".item").length+1);
  $(".source-container,.destination-container").height(height);
  
    

  $(".source .item").draggable({
    revert:"invalid",
    start:function(){
      
      $(this).data("index",$(this).parent().index());
      
    }
  });
  
  $(".destination").droppable({
      drop:function(evern,ui){
          if($(this).has(".item").length){
            if(ui.draggable.parent().hasClass("source")){
                index=ui.draggable.data("index");
                ui.draggable.css({left:"0",top:"0"}).appendTo($(".source").eq(index));
            }
            else{
             ui.draggable.css({left:"0",top:"0"}).appendTo($(this));
              index=ui.draggable.data("index");
              $(this).find(".item").eq(0).appendTo($(".destination").eq(index))
            }
          }
        else{
          ui.draggable.css({left:"1px",top:"1px"});
          ui.draggable.appendTo($(this));
          $(".destination").removeClass("ui-droppable-active");
        }
      }
  });
  
  $(".source").droppable({
    accept: function(draggable) {
        return $(this).find("*").length == 0;
    },
   drop:function(event,ui){
     ui.draggable.css({left:"0",top:"0"}).appendTo($(this))
   }
  })
  
  
  
  
})
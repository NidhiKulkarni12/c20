var movingrect;
var fixedrect;

function setup() {
  createCanvas(800,400);
   movingrect= createSprite(400, 200, 50, 50);
   fixedrect=createSprite(200, 200, 50, 50);
  
}

function draw() {
  background(255,255,255); 
  movingrect.x=World.mouseX;
  movingrect.y=World.mouseY; 

  console.log(movingrect.x-fixedrect.x);
  console.log(fixedrect.x-movingrect.x);
  console.log(fixedrect.width/2+movingrect.width/2);

  movingrect.shapeColor="green";
  fixedrect.shapeColor="blue";
    if(movingrect.x-fixedrect.x<=fixedrect.width/2+movingrect.width/2)
  {
    movingrect.shapeColor="red";
  fixedrect.shapeColor="red";
  }
  //if(fixedrect.x-movingrect.x<=fixedrect.width/2+movingrect.width/2)
  //{
   // movingrect.shapeColor="red";
 // fixedrect.shapeColor="red";
 // }
  if(movingrect.y-fixedrect.y<=fixedrect.width/2+movingrect.width/2)
  {
    movingrect.shapeColor="red";
  fixedrect.shapeColor="red";
  }
 // if(fixedrect.y-movingrect.y<=fixedrect.width/2+movingrect.width/2)
  //{
  //  movingrect.shapeColor="red";
  //fixedrect.shapeColor="red";
  //}
  
  drawSprites();

}
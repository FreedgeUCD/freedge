

camera_x=14.1;
camera_y=12.1;
camera_z=5;

cam_mount_h=5;
cam_mount_y=5;
cam_mount_x=2.5;

cam_mount_hole=1.8;

lens_d=10;
lens_margin=0.5;
wall=1;

$fn=90;
n=0.1;

standoff_distance=25;
standoff_h=20;
standoff_m=1.8;
standoff_w=4.5;

standoff_cam_mount_h=1.5;
standoff_cam_mount_y=5;
standoff_cam_mount_x=1.5;

cam_mount_hole_head=4;

standoff_offset_x=cam_mount_y*0.5+wall;

option_show_case=true;
option_show_standoff=false; //show only one standoff
option_show_standoffs=true;

//Camera Housing

//rotate([-240,0,0])

if(option_show_case)
union() {
    difference() {
        //Housing
        cube([camera_x+wall*2,camera_y+wall*2,camera_z+wall],center=true);

        //Cam inside
        translate([0,0,wall])
            cube([camera_x,camera_y,camera_z],center=true);
        
        //lens
        translate([0,0,-5])
        cylinder(d=lens_d+lens_margin,h=10);
    }

    //Left mount
    translate([-((camera_x+wall*2)*0.5+cam_mount_x),-cam_mount_y*0.5,-cam_mount_h*0.5]) {
        side_mounts();
    }

    //Right
    translate([+((camera_x+wall*2)*0.5),-cam_mount_y*0.5,-cam_mount_h*0.5]) {
        side_mounts();
    }
}

module side_mounts() {
    difference() {
        translate([0,0,-wall*0.5])
        cube([cam_mount_x,cam_mount_y,camera_z]);
       
        //Hole for screw
        rotate([0,90,0])
            translate([-cam_mount_h*0.5,cam_mount_y*0.5,-1])
            cylinder(d=cam_mount_hole,h=5);
    }
        
}

module standoff_solo(h,m,w) {
    difference() {
        cylinder(d=w,h=h,center=true);
        cylinder(d=m,h=h+n,center=true);
    }
}


if(option_show_standoffs) {

///// Standoffs

color([0,0.5,0]) {
    
    difference() {
        hull() {
        //LEFT STANDOFF
        translate([-standoff_distance*0.5,standoff_offset_x,0])
            cylinder(d=standoff_w,h=standoff_h,center=true);

            //Left mount
            translate([-((camera_x+wall*2)*0.5+standoff_cam_mount_x+cam_mount_x),-standoff_cam_mount_y*0.5,-standoff_cam_mount_h*0.5]) {
                cube([standoff_cam_mount_x,standoff_cam_mount_y,standoff_cam_mount_h]);
            }
        }
        
        //Holes
        
        //Standoff
        translate([-standoff_distance*0.5,standoff_offset_x,0])
            cylinder(d=standoff_m,h=standoff_h+n,center=true);
        
        //Mount hole
        //Hole for screw
        translate([-((camera_x+wall*2)*0.5+cam_mount_x+cam_mount_x),-cam_mount_y*0.5,-cam_mount_h*0.5]) {
            rotate([0,90,0])
                translate([-cam_mount_h*0.5,cam_mount_y*0.5,-3])
            {
                //Screw
                cylinder(d=cam_mount_hole,h=10);
            
                //Head
                //HACK
                cylinder(d=cam_mount_hole_head,h=3.4);
            }
        }
    }
    
    //RIGHT STANDOFF
    if(!option_show_standoff)
    difference() {
        hull() 
        {
            translate([standoff_distance*0.5,standoff_offset_x,0])
                cylinder(d=standoff_w,h=standoff_h,center=true);

            //Right
            //translate([((camera_x+wall*2)*0.5)+standoff_cam_mount_x,-standoff_cam_mount_y*0.5,-standoff_cam_mount_h*0.5]) {
            #translate([camera_x*0.5+wall+cam_mount_x,-standoff_cam_mount_y*0.5,-standoff_cam_mount_h*0.5]) {
                cube([standoff_cam_mount_x,standoff_cam_mount_y,standoff_cam_mount_h]);
            }
        }
        
        //Holes
        //Standoff
        translate([standoff_distance*0.5,standoff_offset_x,0])
            cylinder(d=standoff_m,h=standoff_h+n,center=true);
        
       //Hole for screw
        translate([((camera_x+wall*2)*0.5-cam_mount_x+cam_mount_x),-cam_mount_y*0.5,-cam_mount_h*0.5]) {
            rotate([0,90,0])
                translate([-cam_mount_h*0.5,cam_mount_y*0.5,-3]) {
                    
                    //Screw
                    cylinder(d=cam_mount_hole,h=10);
                
                    //Head
                    //HACK
                    translate([0,0,7]) 
                    cylinder(d=cam_mount_hole_head,h=3.4);
                }
        }
    }
}

}
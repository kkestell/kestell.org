a = 58.5 / 2; // diameter of a
c = 97 / 2;   // diameter of c
ah = 25;      // height of a
bh = 50;      // height of b
ch = 25;      // height of c
t = 3;        // wall thickness

// a
translate([0, 0, bh]) {
    linear_extrude(height = ah, $fn = 100) {
        difference() {
            circle(a + t);
            circle(a);
        }
    }
}

// a -> b
linear_extrude(height = bh, scale = (a + t / 2) / c, $fn = 100) {
    difference() {
        circle(c + t);
        circle(c);
    }
}

// b
translate([0, 0, -ch]) {
    linear_extrude(height = ch, $fn = 100) {
        difference() {
            circle(c + t);
            circle(c);
        }
    }
}
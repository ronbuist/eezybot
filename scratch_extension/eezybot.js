/**
 Copyright (c) 2019 Ron Buist All right reserved.
 EEZYbot Scratch extension is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.
 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 */

(function (ext) {
    var socket = null;

    var connected = false;
    var myStatus = 1;						// initially, set light to yellow
    var myMsg = 'not_ready';
    var pixelCount = 0;
    var realPixelCount = 0;

    // General functions.
    function positionLimit (pos) {
        pos = Math.floor(pos);
        pos = parseInt(pos);
        pos = Math.min(180,pos);
        pos = Math.max(0,pos);
        return pos;
    };

    // when the connect to server block is executed.
    ext.cnct = function (hostname, port) {

        window.socket = new WebSocket("ws:" + hostname + ":" + String(port));

	window.socket.onopen = function () {

	        // initialize the EEZYbot server
        	window.socket.send("init");
	};

        // change status light from yellow to green.
        myMsg = 'ready';
        connected = true;
        myStatus = 2;

    };

    // Cleanup function when the extension is unloaded
    ext._shutdown = function () {
        window.socket.onclose = function () {}; // disable onclose handler first
    	window.socket.close(); // close the socket.
    };

    // Status reporting code
    // Use this to report missing hardware, plugin or unsupported browser
    ext._getStatus = function (status, msg) {
        return {status: myStatus, msg: myMsg};
    };

    // when the set neutral block is executed
    ext.setNeutral = function () {
    	var msg = "setneutral";
    	window.socket.send(msg);
    };

    // when the set gripper block is executed
    ext.setGripper = function (pos) {
	//pos = positionLimit (pos);
        var msg = "setgripper " + String(pos);
    	window.socket.send(msg);
    };

    // when the gate block is executed
    ext.setGate = function (action) {
        if (action == "open") {
          window.socket.send("setgate open");
        } else {
          window.socket.send("setgate close");
    	}
    };

    // when the disconnect from server block is executed
    ext.discnct = function () {
        window.socket.onclose = function () {}; // disable onclose handler first
    	window.socket.close();                  // close the socket.
    	socket = null;
        connected = false;
        myMsg = 'not_ready';                    // back to yellow status.
        myStatus = 1;
        pixelCount = 0;
    };

    // Block and block menu descriptions
    var lang = navigator.language || navigator.userLanguage;
    lang = lang.toUpperCase();
    if (lang.includes('NL')) {

        var descriptor = {
            blocks: [
                // Block type, block name, function name
                [" ", 'Verbind met EEZYbot server op %s poort %n.', 'cnct', "Host", "Poort"],
                [" ", 'Verbreek verbinding met EEZYbot server', 'discnct'],
		[" ", 'Arm neutraal', 'setNeutral'],
		["w", 'Grijper positie %n', 'setGripper', "90"],
		[" ", '%m.action hekje', 'setGate', "open"],
		[" ", 'Arm positie %n, %n, %n', 'setArm', "90", "90", "90"]
            ],
            "menus": {
                "action": ["open", "sluit"]

            },
            url: 'https://github.com/ronbuist/eezybot'
        };

    }
    else {

        var descriptor = {
            blocks: [
                // Block type, block name, function name
                [" ", 'Connect to EEZYbot server on host %s and port %n.', 'cnct', "Host", "Port"],
                [" ", 'Disconnect from EEZYbot server', 'discnct'],
		[" ", 'Arm neutraal', 'setNeutral'],
		["w", 'Gripper position %n', 'setGripper', "90"],
		[" ", '%m.action gate', 'setGate', "open"],
		[" ", 'Arm position %n, %n, %n', 'setArm', "90", "90", "90"]
            ],
            "menus": {
                "action": ["open", "close"]

            },
            url: 'https://github.com/ronbuist/eezybot'
        };
    };

    // Register the extension
    ScratchExtensions.register('eezybot', descriptor, ext);
})({});

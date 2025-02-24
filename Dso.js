// ==UserScript==
// @name         Android Touch Virtual Cursor
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Adds a virtual cursor controlled by touch on Android
// @author       Psylo-Dev
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Create the virtual cursor
    let cursor = document.createElement("div");
    cursor.style.position = "fixed";
    cursor.style.width = "20px";
    cursor.style.height = "20px";
    cursor.style.borderRadius = "50%";
    cursor.style.backgroundColor = "red";
    cursor.style.pointerEvents = "none";
    cursor.style.zIndex = "9999";
    document.body.appendChild(cursor);

    let cursorX = window.innerWidth / 2; // Start in center
    let cursorY = window.innerHeight / 2;

    cursor.style.transform = `translate(${cursorX}px, ${cursorY}px)`;

    // Track touch movement
    document.addEventListener("touchmove", (e) => {
        let touch = e.touches[0];
        cursorX = touch.clientX;
        cursorY = touch.clientY;
        cursor.style.transform = `translate(${cursorX}px, ${cursorY}px)`;
    });

    // Simulate click effect on touch
    document.addEventListener("touchstart", (e) => {
        cursor.style.transform += " scale(0.8)";
        setTimeout(() => cursor.style.transform = `translate(${cursorX}px, ${cursorY}px) scale(1)`, 100);

        // Simulate real click
        let touch = e.touches[0];
        let element = document.elementFromPoint(touch.clientX, touch.clientY);
        if (element) {
            element.click();
        }
    });

})();

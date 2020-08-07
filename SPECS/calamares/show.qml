/* === This file is part of Calamares - <https://github.com/calamares> ===
 *
 *   Copyright 2015, Teo Mrnjavac <teo@kde.org>
 *   Copyright 2018, Adriaan de Groot <groot@kde.org>
 *
 *   Calamares is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   Calamares is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with Calamares. If not, see <http://www.gnu.org/licenses/>.
 */

import QtQuick 2.0;
import calamares.slideshow 1.0;

Presentation
{
    id: presentation

    function nextSlide() {
        console.log("Next slide");
        presentation.goToNextSlide();
    }

    Timer {
        id: advanceTimer
        interval: 500
        running: false
        repeat: true
        onTriggered: nextSlide()
    }

    Slide {
        id: slide
        x: presentation.x
        y: presentation.y
        width: presentation.width
        height: presentation.height


        Rectangle {
            width: slide.width
            height: slide.height
            color: "#efefef"
        }

        Image {
            id: background
            fillMode: Image.PreserveAspectFit
            source: "mariner-welcome.png"
            anchors.centerIn: slide
        }

        Text {
            anchors.horizontalCenter: slide.horizontalCenter
            text: qsTr("Installing...")
            color: slide.titleColor
            font.family: slide.fontFamily
            font.pixelSize: slide.titleFontSize
            font.bold: true
            horizontalAlignment: Text.Center
        }
   }

    Component.onCompleted: advanceTimer.running = true
}

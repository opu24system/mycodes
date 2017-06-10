//
//  pockBullet.swift
//  pockyTest
//
//  Created by lab-6h on 2017/01/12.
//  Copyright © 2017年 lab-6h. All rights reserved.
//

import Foundation
import UIKit
import SpriteKit

var pockBulletImg : SKSpriteNode? = SKSpriteNode(imageNamed: "pockBullet")

let pockBulletWidth: CGFloat = pockBulletImg!.size.width/1.5
let pockBulletHeight: CGFloat = pockBulletImg!.size.height/1.5

var screenWidth : CGFloat = UIScreen.main.bounds.size.width
var screenHeight : CGFloat =  UIScreen.main.bounds.size.height

let launchPointX : CGFloat = 0
let launchPointY : CGFloat = pockBulletHeight/2

var LaunchRangeAngle : Float = 45


class PockBullet {
    private var x : CGFloat
    private var y : CGFloat
    private var firstSpeed : Float
    private var speed : Float
    private var rad : Float
    public var ready : Int
    public var out : Int
    public var spNode : SKSpriteNode?

    init(xin : CGFloat , yin : CGFloat , radin : Float, firstSpeedin : Float) {
        self.x = xin
        self.y = yin
        self.rad = radin
        self.firstSpeed = firstSpeedin
        self.speed = self.firstSpeed
        self.ready = 1
        self.out = 0
        if let n = pockBulletImg?.copy() as! SKSpriteNode? {
            n.position = CGPoint(x: xin, y: yin)
            n.size = CGSize(width: pockBulletWidth, height: pockBulletHeight) //ipad
            n.zPosition = 10
            self.spNode = n
            //self.addChild(n)
        }
    }
    
    
    func clone() -> AnyObject {
        let clonePock = PockBullet(xin: self.x, yin: self.y, radin: self.rad, firstSpeedin: speed)
        return clonePock
    }
    
    func initPock(speedin : Float){
        //x = random(launchX, launchW);
        //y = random(launchY, launchH);
        self.x = launchPointX - 50 + (CGFloat)(arc4random_uniform(100)) //- (Int)((self.spNode?.size.width)!)//
        self.y = launchPointY - 50 + (CGFloat)(arc4random_uniform(100)) - (self.spNode?.size.height)!
        
        self.rad = 90 - LaunchRangeAngle / 2 + (Float)(arc4random_uniform(((UInt32)(LaunchRangeAngle))))
        self.speed = firstSpeed + speedin * 2
        
        //print("x: " + String(screenWidth) + " y: " + String(screenHeight))
    }
    
    func upDate(){
        self.speed += 0.05;
        //self.rad += 1
        self.x -= (CGFloat)(self.speed * cos((self.rad + 180) * (Float)(M_PI / 180)))
        self.y -= (CGFloat)(self.speed * sin((self.rad + 180) * (Float)(M_PI / 180)))
    
        if(self.x < -(self.spNode?.size.height)! ||
           self.x > screenWidth + ((self.spNode?.size.height)!) ||
           self.y < -(self.spNode?.size.height)! ||
           self.y > screenHeight + ((self.spNode?.size.height)!)){
            self.ready = 1
            self.out = 1
            self.x = -1000
            self.y = -1000
        }
        self.spNode?.position = CGPoint(x: self.x, y: self.y)
        //self.spNode?.zRotation = (CGFloat)(self.rad + 270) * (CGFloat)(M_PI / 180)
        self.spNode?.zRotation = (CGFloat)(self.rad + 270) * (CGFloat)(M_PI / 180)
        //print(self.x)
    }
    
    func display() {
    //rotateImage(x, y, pockW, pockH, pock, rad);
    }
    
}

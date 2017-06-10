//
//  InputVol.swift
//  pockyTest
//
//  Created by lab-6h on 2017/01/19.
//  Copyright © 2017年 lab-6h. All rights reserved.
//

import Foundation
import SpriteKit

class InputVol {
    public var label : SKLabelNode = SKLabelNode()
    
    public var volumeVal: CGFloat = 0
    public var touchStartPos : CGPoint = CGPoint(x: 0, y: 0)
    private var appearCount: Int = 0
    private var decideTime: Int = 100
    private var decideFlag: Int = 0
    private var flashTime: Int = 120

    init(parentScene : GameScene){
        parentScene.addChild(self.label)
        self.label.isHidden = true
        //self.label.position = CGPoint(x: 0, y: 0)
        self.label.zPosition = 201
        self.label.fontSize = 50
        self.label.text = "InputVol  0"
        self.label.fontColor = UIColor.white
        self.label.fontName = "GeezaPro-Bold"
        
        
    }

    func show(){
        self.label.isHidden = false
    }
    
    func hide(){
        self.label.isHidden = true
    }
    
    func touchStart(position : CGPoint) {
        self.label.isHidden = false
        self.touchStartPos = position
    }
    
    func touchMoved(position : CGPoint) {
        if(decideFlag == 0){
            self.volumeVal += (position.y - self.touchStartPos.y) / 100
            self.touchStartPos = position
        }
        
        if(self.decideFlag != 1 && self.decideFlag != 3){
            self.appearCount = 0
        }
    }
    
    func touchEnd() {
        if(self.decideFlag != 1 && self.decideFlag != 3){
            self.label.isHidden = true
            self.appearCount = 0
        }
    }
    
    func decideValueSeq(){
        if(self.label.isHidden == false){
            self.appearCount += 1
        }
        
        if(self.appearCount >= self.decideTime){
            self.decideFlag = 1
            
            if((appearCount/5) % 2 == 0){
                self.label.isHidden = true
            }else{
                self.label.isHidden = false
            }
            if(self.appearCount - self.decideTime >= self.flashTime){
                self.appearCount = 0
                self.decideFlag = 2
            }
            self.appearCount += 1
        }
    }
    
    func unlockDecideSeq(){
        if(self.label.isHidden == false){
            self.appearCount += 1
        }
        
        if(self.appearCount >= self.decideTime){
            self.decideFlag = 3
            
            self.label.fontColor = UIColor.green
            
            if((appearCount/5) % 2 == 0){
                self.label.isHidden = true
            }else{
                self.label.isHidden = false
            }
            if(self.appearCount - self.decideTime >= self.flashTime){
                self.appearCount = 0
                self.decideFlag = 0
                
                self.label.fontColor = UIColor.white
            }
            self.appearCount += 1
        }
    }
    
    func update(){
        let vol = self.volumeVal * 10
        self.label.text = "InputVol  " + String((Float)(floor(vol)/10))
        
        if(decideFlag == 0 || decideFlag == 1){
            self.decideValueSeq()
        }
        if(decideFlag == 2 || decideFlag == 3){
            self.unlockDecideSeq()
        }
        
    }
}

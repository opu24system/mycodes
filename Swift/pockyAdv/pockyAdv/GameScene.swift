//
//  GameScene.swift
//  pockyTest
//
//  Created by lab-6h on 2017/01/12.
//  Copyright © 2017年 lab-6h. All rights reserved.
//

import SpriteKit
import GameplayKit

let numPockies : Int = 100
//var micLevel : Float = -10

class GameScene: SKScene {
    
    private var label : SKLabelNode?
    private var spinnyNode : SKShapeNode?
    
    private var pockBg = SKSpriteNode(imageNamed: "pockBack")
    private var pockBox = SKSpriteNode(imageNamed: "pockBoxSmall")
    private var oishiImg = SKSpriteNode(imageNamed: "oishikute")
    private var tsuyoImg = SKSpriteNode(imageNamed: "tsuyoshi")
    private var pockImg = SKSpriteNode(imageNamed: "pockBullet")
    
    private var inputVol: InputVol? = nil
    
    private var pockBulletMaster = PockBullet(xin: 0, yin: 0, radin: 0, firstSpeedin: 0)
    private var pockBullets = [PockBullet]()
    private var pockBulletsMovin = [PockBullet]()
    private var addCount : Int = 0
    
    private var levelSusFlag : Int = 0
    private var levelSusFlagOld : Int = 0
    private var cntLevel = [Int](arrayLiteral: 0, 0, 0, 0, 0, 0)
    private var levelSusCount  = [Int](arrayLiteral: 0,0,0,0,0,0)
    private var levelSusTime = [Int](arrayLiteral: 15,15,15,15,120,1200)
    
    private var deliFlag : Bool = false
    private var deliCount : Int = 0
    private var deliDuration: Int = 120
        
    override func didMove(to view: SKView) {
        
        self.backgroundColor = SKColor.gray
        
        //背景画像の設定
        self.pockBg.position = CGPoint(x: 0, y: 0)
        
        self.pockBg.size = CGSize(width: screenWidth, height: screenHeight)//ipad
        //self.pockBg.size = CGSize(width: size.width * 1.2, height: size.height)// iphone
        self.pockBg.zPosition = 0
        self.addChild(pockBg)
        
        //ポッキーの箱
        self.pockBox.position = CGPoint(x: 0, y: -self.pockBox.size.height/3.6) //ipad
        self.pockBox.size = CGSize(width: self.pockBox.size.width/1.35, height: self.pockBox.size.height/1.35)//ipad
        
        //self.pockBox.position = CGPoint(x: 0, y: -size.height/4) //iphone
        //self.pockBox.size = CGSize(width: size.width/1.2, height: size.height/1.5) //iphone
        self.pockBox.zPosition = 100
        self.addChild(pockBox)
        
        //美味しくて強くなるやつ
        self.oishiImg.position = CGPoint(x: 0, y: 250)
        self.oishiImg.xScale = 0.622
        self.oishiImg.yScale = 0.622
        //self.oishiImg.size = CGSize(width: size.width, height: size.height)
        self.oishiImg.zPosition = 101
        self.addChild(oishiImg)
        self.oishiImg.alpha = 0.0
        
        self.tsuyoImg.position = CGPoint(x: 0, y: -self.tsuyoImg.size.height*1.5)//ipad
        //self.tsuyoImg.position = CGPoint(x: 0, y: -self.tsuyoImg.size.height*2)//iphone
        //self.tsuyoImg.size = CGSize(width: size.width, height: size.height/2)
        self.tsuyoImg.zPosition = 102
        self.addChild(tsuyoImg)
        self.tsuyoImg.alpha = 0.0
        
        //Masterのクローンポッキーをたくさん生産
        for _ in 0..<numPockies {
            let newPock = self.pockBulletMaster.clone() as! PockBullet
            newPock.spNode?.isHidden = true
            pockBullets.append(newPock)
            
            newPock.initPock(speedin: 3.0)
            self.addChild(newPock.spNode!)
        }
        
        //マイク入力音量の調整用ラベルを設定
        inputVol = InputVol(parentScene: self)
        //inputVol!.show()
        
        
        /*
        // Get label node from scene and store it for use later
        self.label = self.childNode(withName: "//helloLabel") as? SKLabelNode
        if let label = self.label {
            label.alpha = 0.0
            label.run(SKAction.fadeIn(withDuration: 2.0))
        }
 
        */
        // Create shape node to use during mouse interaction
        let w = (self.size.width + self.size.height) * 0.05
        self.spinnyNode = SKShapeNode.init(rectOf: CGSize.init(width: w, height: w), cornerRadius: w * 0.3)
        
        if let spinnyNode = self.spinnyNode {
            spinnyNode.lineWidth = 2.5
            spinnyNode.zPosition = 50
            
            spinnyNode.run(SKAction.repeatForever(SKAction.rotate(byAngle: CGFloat(M_PI), duration: 1)))
            spinnyNode.run(SKAction.sequence([SKAction.wait(forDuration: 0.5),
                                              SKAction.fadeOut(withDuration: 0.5),
                                              SKAction.removeFromParent()]))
        }
 
    }
    
    
    func touchDown(atPoint pos : CGPoint) {
        /*
        if let n = self.spinnyNode?.copy() as! SKShapeNode? {
            n.position = pos
            n.strokeColor = SKColor.green
            self.addChild(n)
            
            print("x:" + String(describing: pos.x), " y:" + String(describing: pos.y))
        }
        */
        self.inputVol?.touchStart(position: pos)
    }
    
    func touchMoved(toPoint pos : CGPoint) {
        /*
        if let n = self.spinnyNode?.copy() as! SKShapeNode? {
            n.position = pos
            n.strokeColor = SKColor.blue
            self.addChild(n)
        }
        */
        
        self.inputVol?.touchMoved(position: pos)
    }
    
    
    func touchUp(atPoint pos : CGPoint) {
        /*
        if let n = self.spinnyNode?.copy() as! SKShapeNode? {
            n.position = pos
            n.strokeColor = SKColor.red
            self.addChild(n)
        }
 */
        self.inputVol?.touchEnd()
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        
        for t in touches { self.touchDown(atPoint: t.location(in: self)) }
    }
    
    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent?) {
        for t in touches { self.touchMoved(toPoint: t.location(in: self)) }
    }
    
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        for t in touches { self.touchUp(atPoint: t.location(in: self)) }
    }
    
    override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent?) {
        for t in touches { self.touchUp(atPoint: t.location(in: self)) }
    }
    
    func levelSusUpdate(){
        self.levelSusFlagOld = self.levelSusFlag
        let mcLevel : Float = micIn.mAverage + (Float)((inputVol?.volumeVal)!)
        //print(String(mcLevel))

        if(mcLevel < -50){
            //addPockiesLevel(2);
        }
        if(mcLevel >= -50 && mcLevel <= -30){
            self.levelSusFlag = 1;
        }
        if(mcLevel > -30 && mcLevel <= -20){
            self.levelSusFlag = 2;
        }
        if(mcLevel > -20 && mcLevel <= -10){
            self.levelSusFlag = 3;
        }
        if(mcLevel > -10 && mcLevel <= -5){
            self.levelSusFlag = 4;
        }
        if(mcLevel > -5 ){
            self.levelSusFlag = 5;
        }
        
        if(self.levelSusFlag >= 1){
            if(self.levelSusFlagOld >= 4){
                self.levelSusFlag = self.levelSusFlagOld
            }
            
            let flag : Int = self.levelSusFlag - 1;
            self.levelSusCount[flag] += 1;
            //print(self.levelSusFlag)
    
            if(self.levelSusCount[flag] >= self.levelSusTime[flag]){
                
                //print(self.levelSusCount[flag])
                self.levelSusCount[flag] = 0;
                self.levelSusFlag = 0;
            }
            
            if(self.levelSusFlagOld >= 1 && self.levelSusFlagOld != self.levelSusFlag){
                self.levelSusCount[self.levelSusFlagOld - 1] = 0;
            }
        }
        
        if(levelSusFlag == 5){
            self.deliFlag = true
            self.deliCount = 0
            self.DeliciousAndStrongIn()
        }else{
            if(self.deliFlag == true){
                self.deliCount += 1
                if(self.deliCount >= self.deliDuration){
                    self.DeliciousAndStrongOut()
                    self.deliFlag = false
                    self.deliCount = 0
                }
            }
        }
        
        switch(levelSusFlag){
        case 0: addPockiesLevel(level: 2); break;
        case 1: addPockiesLevel(level: 2); break;
        case 2: addPockiesLevel(level: 2); break;
        case 3: addPockiesLevel(level: 2); break;
            
        case 4: addPockiesLevel(level: 2); break;//addPockiesLevel(level: 5); break;
        case 5: addPockiesLevel(level: 4); addPockiesLevel(level: 5); addPockiesLevel(level: 6); break;//addPockiesLevel(level: 6); break;
        default: break;
        }
    }
    
    func  addPockiesLevel(level : Int){
        var lInterval: Int = 9
        var fSpeed: Float = 4
        
        self.cntLevel[level-1] += 1;
        if(self.cntLevel[level-1] / lInterval > 1000000){
            self.cntLevel[level-1] = 0;
        }
        
        switch(level){
            
        case 1: lInterval = 20; fSpeed = 1; break;
        case 2: lInterval = 16; fSpeed = 2; break;
        case 3: lInterval = 12; fSpeed = 3; break;
            
        case 4: lInterval = 9; fSpeed = 3; break;
        case 5: lInterval = 9; fSpeed = 5; break;
        case 6: lInterval = 5; fSpeed = 10; break;
        //case 6: lInterval = 1; fSpeed = 10; break;
        //case 16: lInterval = 16; fSpeed = 10; break;
        default:  lInterval = 5; fSpeed = 5; break;
        }
        
        if(cntLevel[level-1] % lInterval == 0){
            for element in pockBullets{
                if(element.ready == 1){
                    pockBulletsMovin.append(element)
                    element.initPock(speedin: fSpeed)
                    element.spNode?.isHidden = false
                    //element.spNode?.
                    element.ready = 0
                    element.out = 0
                    self.addCount += 1;
                    break;
                }
            }
        }
    }
    
    func DeliciousAndStrongIn(){
        let fadeInTime: Double = 1.0
        //let tsuyoWaitTime: Double = 0.5
        self.oishiImg.run(SKAction.sequence([SKAction.fadeIn(withDuration: fadeInTime),
                                             ]))
        
       // self.tsuyoImg.run(SKAction.sequence([SKAction.wait(forDuration: tsuyoWaitTime),
                                             //SKAction.fadeIn(withDuration: fadeInTime)
                                             //]))
 
    }
    
    func DeliciousAndStrongOut(){
        let fadeOutTime: Double = 2.0
        self.oishiImg.run(SKAction.sequence([SKAction.fadeOut(withDuration: fadeOutTime)]))
        //self.tsuyoImg.run(SKAction.sequence([SKAction.fadeOut(withDuration: fadeOutTime)]))
    }
    
    override func update(_ currentTime: TimeInterval) {
        // Called before each frame is rendered
        
        //self.pockImg.position.y += 1;
        //self.pockImg.zRotation += 0.1;
        
        self.levelSusUpdate()
        
        if(pockBulletsMovin.count >= 1){
            for i in (0..<pockBulletsMovin.count).reversed(){
                pockBulletsMovin[i].upDate()
                if(pockBulletsMovin[i].out == 1){
                    pockBulletsMovin[i].spNode?.isHidden = true
                    pockBulletsMovin.remove(at: i)
                }
            }
        }
        inputVol?.update()
    }
}



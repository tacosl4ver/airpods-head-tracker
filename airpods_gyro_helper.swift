import CoreMotion
import Foundation

let manager = CMHeadphoneMotionManager()

// -psn_XXXXXX (LaunchServices が open 経由起動時に挿入) を除いた最初の非フラグ引数を FIFO パスとして使う
let fifoPath = CommandLine.arguments.dropFirst()
    .first(where: { !$0.hasPrefix("-") })

// FIFO があれば先に開く（Python 側が open(FIFO,'r') でブロック解除されるよう）
var outputHandle: FileHandle = .standardOutput
if let path = fifoPath,
   let fh = FileHandle(forWritingAtPath: path) {
    outputHandle = fh
}

guard manager.isDeviceMotionAvailable else {
    let msg = "{\"status\":\"unavailable\"}\n"
    if let data = msg.data(using: .utf8) { outputHandle.write(data) }
    exit(1)
}

manager.startDeviceMotionUpdates(to: OperationQueue()) { motion, error in
    guard let motion = motion else { return }
    let att = motion.attitude
    let line = String(format: "{\"yaw\":%.3f,\"pitch\":%.3f,\"roll\":%.3f}\n",
                      att.yaw * 180.0 / .pi,
                      att.pitch * 180.0 / .pi,
                      att.roll * 180.0 / .pi)
    if let data = line.data(using: .utf8) {
        outputHandle.write(data)
    }
}

RunLoop.main.run()

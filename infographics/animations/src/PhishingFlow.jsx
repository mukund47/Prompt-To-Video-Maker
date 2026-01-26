import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';
import { Mail, User, Lock, ArrowRight, AlertTriangle } from 'lucide-react';
import React from 'react';

const Icon = ({ icon: IconComponent, color, x, y, scale = 1, opacity = 1 }) => {
    return (
        <div style={{
            position: 'absolute',
            left: x,
            top: y,
            transform: `scale(${scale})`,
            opacity: opacity,
            color: color,
        }}>
            <IconComponent size={100} />
        </div>
    );
};

export const PhishingFlow = () => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // Animation timings
    const emailAppear = 0;
    const arrow1Appear = 30;
    const userAppear = 60;
    const clickAction = 90;
    const theftAction = 120;

    // Opacities
    const emailOpacity = Math.min(1, (frame - emailAppear) / 15);
    const arrow1Opacity = Math.min(1, (frame - arrow1Appear) / 15);
    const userOpacity = Math.min(1, (frame - userAppear) / 15);

    // Dynamic styles
    const emailX = interpolate(frame, [0, 30], [200, 300], { extrapolateRight: 'clamp' });
    const redFlash = frame > clickAction && frame < theftAction && frame % 10 < 5 ? 'red' : 'white';

    return (
        <AbsoluteFill style={{ backgroundColor: '#1a1a2e', justifyContent: 'center', alignItems: 'center' }}>
            <h1 style={{ color: 'white', position: 'absolute', top: 50, fontFamily: 'Arial' }}>Phishing Attack Flow</h1>

            {/* Step 1: Malicious Email */}
            <Icon icon={Mail} color="#e94560" x={emailX} y={400} opacity={emailOpacity} />
            {emailOpacity > 0.8 && <div style={{ position: 'absolute', left: emailX, top: 520, color: '#e94560' }}>Fake Email</div>}

            {/* Arrow 1 */}
            <div style={{ position: 'absolute', left: 550, top: 430, opacity: arrow1Opacity }}>
                <ArrowRight size={80} color="white" />
            </div>

            {/* Step 2: User */}
            <Icon icon={User} color="white" x={800} y={400} opacity={userOpacity} />
            {userOpacity > 0.8 && <div style={{ position: 'absolute', left: 810, top: 520, color: 'white' }}>Victim</div>}

            {/* Step 3: The Attack */}
            {frame > clickAction && (
                <>
                    <Icon icon={AlertTriangle} color="#ffd700" x={800} y={250} scale={1.5} />
                    <div style={{
                        position: 'absolute',
                        left: 0,
                        top: 0,
                        width: '100%',
                        height: '100%',
                        border: `10px solid ${redFlash}`,
                        opacity: 0.5
                    }} />
                    <h2 style={{ position: 'absolute', bottom: 100, color: '#e94560', fontSize: 60 }}>DATA STOLEN</h2>
                </>
            )}

        </AbsoluteFill>
    );
};

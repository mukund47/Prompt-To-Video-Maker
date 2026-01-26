import { registerRoot } from 'remotion';
import { Composition } from 'remotion';
import { PhishingFlow } from './PhishingFlow.jsx';

export const RemotionRoot = () => {
    return (
        <>
            <Composition
                id="PhishingFlow"
                component={PhishingFlow}
                durationInFrames={240}
                fps={30}
                width={1920}
                height={1080}
            />
        </>
    );
};

registerRoot(RemotionRoot);

import { HeroGeometric } from "../src/components/ui/shape-landing-hero";
import { MatchPredictor } from "../src/components/ui/match-predictor";

export default function Home() {
  return (
    <HeroGeometric 
        badge="AI Powered Analytics" 
        title1="FIFA World Cup" 
        title2="AI Predictor"
    >
        <MatchPredictor />
    </HeroGeometric>
  );
}

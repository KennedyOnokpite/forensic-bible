import { browser } from '$app/environment';

export interface AudioQueueItem {
    text: string;
    unitIndex: number;
    lang: string;
}

class AudioStore {
    isPlaying = $state(false);
    isPaused = $state(false);
    currentText = $state<string | null>(null);
    currentUnitIndex = $state<number | null>(null);
    progress = $state(0);
    speed = $state(1.0);
    pitch = $state(1.0);
    voice = $state<SpeechSynthesisVoice | null>(null);
    availableVoices = $state<SpeechSynthesisVoice[]>([]);
    queue = $state<AudioQueueItem[]>([]);
    continuous = $state(false);

    private synth: SpeechSynthesis | null = null;
    private currentUtterance: SpeechSynthesisUtterance | null = null;

    constructor() {
        if (browser) {
            this.synth = window.speechSynthesis;
            const loadVoices = () => {
                this.availableVoices = this.synth?.getVoices() || [];
            };

            if (this.synth) {
                if (this.synth.onvoiceschanged !== undefined) {
                    this.synth.onvoiceschanged = loadVoices;
                }
                loadVoices();
            }
        }
    }

    setSpeed(speed: number) {
        this.speed = speed;
    }

    setVoice(voice: SpeechSynthesisVoice) {
        this.voice = voice;
    }

    playText(text: string, unitIndex: number, lang: string = 'en-US') {
        if (!this.synth) return;

        this.synth.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = lang;
        utterance.rate = this.speed;
        utterance.pitch = this.pitch;
        
        // Find specific voice if not set
        if (!this.voice) {
            const voices = this.availableVoices;
            
            // Map common biblical language codes to available TTS codes
            const langMap: Record<string, string[]> = {
                'he-IL': ['he-IL', 'he'],
                'el-GR': ['el-GR', 'el', 'gr'],
                'grc': ['el-GR', 'el', 'gr'], // Ancient Greek fallback to Modern Greek
                'arc': ['he-IL', 'he'],       // Aramaic fallback to Hebrew
                'en-US': ['en-US', 'en-GB', 'en']
            };

            const targetLangs = langMap[lang] || [lang];
            
            let foundVoice = voices.find(v => targetLangs.some(l => v.lang.toLowerCase().replace('_', '-') === l.toLowerCase()) && v.localService);
            if (!foundVoice) {
                foundVoice = voices.find(v => targetLangs.some(l => v.lang.toLowerCase().startsWith(l.split('-')[0].toLowerCase())));
            }
            
            if (foundVoice) utterance.voice = foundVoice;
        } else {
            utterance.voice = this.voice;
        }

        utterance.onstart = () => {
            this.isPlaying = true;
            this.isPaused = false;
            this.currentUnitIndex = unitIndex;
            this.currentText = text;
        };

        utterance.onend = () => {
            if (this.queue.length > 0) {
                const next = this.queue[0];
                this.queue = this.queue.slice(1);
                setTimeout(() => this.playText(next.text, next.unitIndex, next.lang), 100);
            } else if (this.continuous) {
                // Dispatch event to page to play next unit
                window.dispatchEvent(new CustomEvent('audio-unit-ended', { detail: { index: this.currentUnitIndex } }));
                this.isPlaying = false;
            } else {
                this.isPlaying = false;
                this.currentUnitIndex = null;
                this.currentText = null;
                this.progress = 0;
            }
        };

        utterance.onboundary = (event) => {
            if (event.name === 'word') {
                this.progress = event.charIndex / text.length;
            }
        };

        utterance.onerror = (e) => {
            console.error('TTS Error:', e);
            this.isPlaying = false;
        };

        this.currentUtterance = utterance;
        this.synth.speak(utterance);
    }

    pausePlayback() {
        if (this.synth) {
            this.synth.pause();
            this.isPaused = true;
        }
    }

    resumePlayback() {
        if (this.synth) {
            this.synth.resume();
            this.isPaused = false;
        }
    }

    stopPlayback() {
        if (this.synth) {
            this.synth.cancel();
            this.isPlaying = false;
            this.isPaused = false;
            this.currentUnitIndex = null;
            this.currentText = null;
            this.progress = 0;
            this.queue = [];
        }
    }

    addToQueue(text: string, unitIndex: number, lang: string) {
        this.queue.push({ text, unitIndex, lang });
    }
}

export const audioStore = new AudioStore();

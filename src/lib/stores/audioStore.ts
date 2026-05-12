import { writable } from 'svelte/store';

export const isPlaying = writable(false);
export const currentPlayingIndex = writable<number | null>(null);

let synth: SpeechSynthesis;
if (typeof window !== 'undefined') {
    synth = window.speechSynthesis;
}

export function playText(text: string, lang: string = 'en-US') {
    if (!synth) return;

    // Cancel any current speech
    synth.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    
    // Attempt to find a suitable voice
    const voices = synth.getVoices();
    let voice = voices.find(v => v.lang.startsWith(lang));
    
    if (lang === 'el' || lang === 'grc') {
        // Look for Greek voices
        voice = voices.find(v => v.lang.includes('el') || v.lang.includes('gr'));
    }

    if (voice) {
        utterance.voice = voice;
    }

    utterance.onstart = () => isPlaying.set(true);
    utterance.onend = () => isPlaying.set(false);
    utterance.onerror = () => isPlaying.set(false);

    synth.speak(utterance);
}

export function stopPlayback() {
    if (synth) {
        synth.cancel();
        isPlaying.set(false);
        currentPlayingIndex.set(null);
    }
}

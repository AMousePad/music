\version "2.24.0"
\language "english"
\header {
  title = "Nocturne"
  subtitle = "in B minor"
  composer = "Claude, 2026"
  poet = "in the manner of Chopin's nocturnes"
  tagline = ##f
}
\paper {
  #(set-paper-size "a4")
  top-margin = 12\mm  bottom-margin = 12\mm  left-margin = 13\mm  right-margin = 13\mm
  system-system-spacing.basic-distance = #17
  ragged-last-bottom = ##f
}
upper = {
  \clef treble \time 12/8 \tempo "Lento sostenuto" 4. = 46
  \override TupletBracket.bracket-visibility = ##f
  \key b \minor R1. | % 1
   fs''2.\p^\markup\italic"cantabile" g''4 fs''8 e''8 fs''8 b''8 | % 2
   a''4. g''4 fs''8 e''4. g''4 e''8 | % 3
   d''4\< cs''8 d''8 fs''8 b''8 d'''4.\! b''8.\> as''16 a''8 | % 4
   g''4. es''4. fs''4\! d''8 cs''4~ cs''16 fs''16 | % 5
   fs''4.~\p fs''4 fs''8 \acciaccatura a''8 g''4 fs''8 e''8. fs''16 b''8 | % 6
   a''4. g''4 fs''8 e''4 fs''32 e'' ds'' e'' g''4 e''8 | % 7
   d''4\< cs''8 d''8 fs''8 b''8 e'''4.\mf d'''4 b''8 | % 8
   a''4\> g''16 fs''16 e''4~\trill e''16 d''32 e'' d''4.\! fs''8 g''8 gs''8 | % 9
   a''4.\mp^\markup\italic"poco animato" a'8 fs''8 d'''8 c'''4 b''8 a''4 fs''8 | % 10
   b''4.\< b'8 g''8 e'''8 d'''4 cs'''8 b''4 gs''8 | % 11
   d'''4. b''8 cs'''8 d'''8 e'''4.\f d'''8 cs'''8 b''8 | % 12
   as''4.\> cs'''4 as''8 e''4.\!^\markup\italic"rit." g''4 es''8 | % 13
   \acciaccatura fs'8 fs''2.\pp^\markup\italic"a tempo, sotto voce" g''4 fs''8 e''16 fs'' as'' b'' cs''' b'' | % 14
   a''4. g''4 fs''8 \tuplet 17/24 { e''32^\markup\italic"leggiero" fs'' gs'' as'' b'' cs''' d''' e''' fs''' e''' d''' cs''' b'' as'' g'' fs'' e'' } | % 15
   d''4 cs''8 b'8 fs''8 b''8 cs'''4.\mp b''8 a''8 g''8 | % 16
   fs''4\>^\markup\italic"rit." e''16 d''16 cs''8. as'8 b'16 b'2.\! \bar "||" | % 17
  \key g \major <g' b'>4\pp^\markup{\bold"Poco più mosso" \italic" dolce"} <b' d''>8 <b' g''>4. <d'' fs''>4 <c'' e''>8 <b' d''>4. | % 18
   <b' d''>4 <b' e''>8 <d'' b''>4. <c'' a''>4 <c'' e''>8 <a' c''>4. | % 19
   <a' c''>4 <a' d''>8 \acciaccatura b''8 <c'' a''>4. <b' g''>4 <b' d''>8 <g' b'>4. | % 20
   << { \voiceOne <c'' e''>4 <e'' g''>8 <e'' a''>8. gs''16 <e'' g''>8 fs''2. } \new Voice { \voiceTwo s2. d''4. c''4. } >> \oneVoice | % 21
   <g' b'>4 <b' d''>8 <d'' b''>4. <c'' a''>4 <c'' fs''>8 <b' g''>4. | % 22
   <b' d''>4 <b' e''>8 <d'' b''>4. <c'' a''>4\< <e'' c'''>16 ds'''16 <a'' e'''>4. | % 23
   <b'' d'''>4.\mf <a'' c'''>8 <g'' b''>8 <d'' g''>8 <c'' a''>4.\> <c'' b''>8 <c'' a''>8 <d'' fs''>16 g''16 | % 24
   <b' g''>2.\p r4 d'''8 g'''4. | % 25
   <g' b'>4\p^\markup\italic"poco a poco cresc. e stringendo" <b' d''>8 <b' g''>4. <d'' f''>4 <b' e''>8 <b' d''>4. | % 26
   <a' c''>4 <c'' e''>8 <c'' a''>4. <e'' g''>4 <cs'' fs''>8 <cs'' e''>4. | % 27
   <b' d''>4 <d'' fs''>8 <d'' b''>4. <b'' d'''>4. <d''' f'''>4. | % 28
   <e'' g'' e'''>4.\f <c'' c'''>4 <e'' e'''>8 <e'' g'' e'''>4. <cs'' cs'''>4 <e'' e'''>8 | % 29
   <fs'' b'' fs'''>4. <d'' d'''>4 <fs'' fs'''>8 <a'' fs''' a'''>4.\< <fs'' fs'''>4 <a'' a'''>8 | % 30
   <g'' b'' e''' g'''>4.\ff^\markup\italic"allargando"\arpeggio <e'' e'''>4 <g'' g'''>8 <g'' b'' d''' g'''>4.\arpeggio <g'' b'' d''' g'''>4. | % 31
   <fs'' b'' d''' fs'''>4.^\markup\italic"largamente"\arpeggio <e'' e'''>8 <d'' d'''>8 <cs'' cs'''>8 <b' e'' b''>4 <as' e'' as''>8 <cs'' e'' cs'''>4 <e'' as'' e'''>8 | % 32
   <as'' cs''' e''' g'''>4.\fermata\>\arpeggio \tuplet 23/18 { fs'''16\!^\markup\italic"dim. e rall." es''' fs''' g''' fs''' e''' d''' cs''' b'' as'' g'' fs'' e'' d'' cs'' b' as' b' cs'' d'' ds'' e'' es'' } \bar "||" | % 33
  \key b \minor fs''4.~\pp^\markup{\bold"Tempo I"} fs''4 fs''8 g''8. a''16 fs''8 \tuplet 7/6 { e''16 fs'' as'' b'' d''' cs''' b'' } | % 34
   a''4. g''4 fs''8 \tuplet 23/24 { e''32^\markup\italic"leggierissimo" g'' fs'' es'' fs'' gs'' as'' b'' cs''' d''' e''' g''' fs''' es''' fs''' e''' d''' cs''' b'' as'' g'' fs'' e'' } | % 35
   d''4 cs''8 d''8 fs''8 b''8 d'''4~\trill d'''16 cs'''32 d''' b''4 a''8 | % 36
   g''4 a''32 g'' fs'' g'' es''4. fs''4 d''8 cs''4. | % 37
   d''4\p\< cs''8 b'8 b''8 e'''8 e'''4.\mf d'''4 b''8 | % 38
   g''4.\pp^\markup\italic"sotto voce" g'8 e''8 c'''8 e'''4. \tuplet 7/6 { d'''16 c''' b'' c''' e''' d''' c''' } | % 39
   as''4. cs'''4 e'''8 d'''4.\>^\markup\italic"rit." cs'''4 as''16 b''16 \bar "||" | % 40
   b''2.\pp^\markup\italic"a tempo, tranquillo" r4. e''8 fs''8 b''8 | % 41
   a''4. g''4 fs''8 e''4. g''4 e''8 | % 42
  \key b \major ds''4\pp^\markup\italic"dolcissimo" cs''8 ds''8 fs''8 b''8 ds'''4. b''4 gs''8 | % 43
   gs''4. e''4. fs''4 ds''8 b'4. | % 44
   <e'' g''>4.\>^\markup\italic"perdendosi" <ds'' fs''>4. <e' g'>4. <ds' fs'>4.\! | % 45
   r8 b'8\ppp ds''8 fs''8 b''8 ds'''8 fs'''8 b'''4~ b'''4. | % 46
   <fs' b' ds''>2.\arpeggio <ds' fs' b'>2.\fermata\arpeggio | % 47
  \bar "|."
}
lower = {
  \clef bass \time 12/8
  \override TupletBracket.bracket-visibility = ##f
  \key b \minor b,,8\pp_\markup\italic"con pedale" fs,8 d8 fs8 b8 fs8 b,,8 fs,8 d8 fs8 d'8 fs8 | % 1
   b,,8 fs,8 d8 fs8 b8 fs8 b,,8 fs,8 d8 fs8 b8 fs8 | % 2
   b,,8 g,8 e8 g8 cs'8 g8 as,,8 fs,8 e8 fs8 cs'8 fs8 | % 3
   b,,8 fs,8 d8 fs8 b8 fs8 g,,8 d,8 b,8 d8 g8 d8 | % 4
   g,,8 e8 b8 g,8 b,8 g8 fs,,8 cs,8 as,8 cs8 fs8 cs8 | % 5
   b,,8 fs,8 d8 fs8 b8 fs8 b,,8 fs,8 d8 fs8 d'8 fs8 | % 6
   b,,8 g,8 e8 g8 cs'8 g8 as,,8 fs,8 e8 fs8 cs'8 fs8 | % 7
   b,,8 fs,8 d8 fs8 b8 fs8 gs,,8 e,8 d8 e8 b8 e8 | % 8
   a,,8 d8 fs8 a,8 cs8 g8 d,8 a,8 fs8 a8 d'8 a8 | % 9
   d,8 a,8 fs8 a8 d'8 a8 ds,8 b,8 fs8 a8 b8 a8 | % 10
   e,8 b,8 g8 b8 e'8 b8 es,8 cs8 gs8 b8 cs'8 b8 | % 11
   fs,,8 fs,8 d8 fs8 b8 fs8 fs,,8 cs,8 as,8 e8 fs8 e8 | % 12
   fs,,8 cs,8 as,8 e8 g8 e8 fs,,8 cs,8 as,8 e8 cs8 as,8 | % 13
   b,,8 fs,8 d8 fs8 b8 fs8 b,,8 fs,8 d8 fs8 d'8 fs8 | % 14
   b,,8 g,8 e8 g8 cs'8 g8 as,,8 fs,8 e8 fs8 cs'8 fs8 | % 15
   b,,8 fs,8 d8 ds,8 b,8 a8 e,8 b,8 g8 b8 e'8 b8 | % 16
   fs,,8 d8 b8 fs,8 cs8 e8 b,,8 fs,8 d8 fs8 b8 fs8 \bar "||" | % 17
  \key g \major g,8 d8 b8 d8 b8 d8 g,8 d8 c'8 g,8 d8 b8 | % 18
   gs,8 e8 b8 e8 d'8 e8 a,8 e8 c'8 e8 c'8 e8 | % 19
   fs,8 d8 c'8 d8 a8 d8 g,8 d8 b8 d8 b8 d8 | % 20
   c8 g8 e'8 cs8 g8 e'8 d8 a8 fs'8 a8 c'8 a8 | % 21
   g,8 d8 b8 d8 b8 d8 g,8 d8 c'8 g,8 d8 b8 | % 22
   gs,8 e8 b8 e8 d'8 e8 a,8 e8 c'8 e8 c'8 e8 | % 23
   d,8 b,8 g8 b8 d'8 b8 d,8 a,8 fs8 c'8 fs8 a,8 | % 24
   g,8 d8 b8 d8 b8 d8 g,8 d8 b8 d8 g8 d8 | % 25
   g,8 d8 b8 d8 b8 d8 gs,8 e8 b8 e8 d'8 e8 | % 26
   a,8 e8 c'8 e8 c'8 e8 as,8 fs8 cs'8 fs8 e'8 fs8 | % 27
   b,8 fs8 d'8 fs8 d'8 fs8 b,8 g8 f'8 g8 d'8 g8 | % 28
   c,8 g,8 e8 g8 c'8 g8 cs,8 as,8 e8 g8 cs'8 g8 | % 29
   d,8 b,8 fs8 b8 d'8 b8 ds,8 b,8 fs8 a8 b8 a8 | % 30
   <e,, e,>8\arpeggio b,8 g8 b8 e'8 b8 <es,, es,>8\arpeggio b,8 d8 g8 b8 d'8 | % 31
   <fs,, fs,>8\arpeggio d8 fs8 b8 d'8 b8 <fs,, fs,>8 cs8 e8 as8 cs'8 as8 | % 32
   <fs,, fs,>8\arpeggio cs8 e8 g8 as8 r8 r2. \bar "||" | % 33
  \key b \minor b,,8 fs,8 d8 fs8 b8 fs8 b,,8 fs,8 d8 fs8 d'8 fs8 | % 34
   b,,8 g,8 e8 g8 cs'8 g8 as,,8 fs,8 e8 fs8 cs'8 fs8 | % 35
   b,,8 fs,8 d8 fs8 b8 fs8 g,,8 d,8 b,8 d8 g8 d8 | % 36
   g,,8 e8 b8 g,8 b,8 g8 fs,,8 cs,8 as,8 cs8 fs8 cs8 | % 37
   b,,8 fs,8 d8 ds,8 b,8 a8 e,8 b,8 g8 b8 e'8 b8 | % 38
   e,8 c8 g8 c'8 e'8 c'8 e,8 c8 g8 c'8 e'8 c'8 | % 39
   fs,,8 cs,8 as,8 e8 fs8 e8 fs,,8 cs,8 as,8 e8 fs8 cs8 \bar "||" | % 40
   b,,8 fs,8 d8 fs8 b8 fs8 b,,8 fs,8 d8 fs8 b8 fs8 | % 41
   b,,8 g,8 e8 g8 cs'8 g8 b,,8 fs,8 e8 as8 cs'8 as8 | % 42
  \key b \major b,,8 fs,8 ds8 fs8 b8 fs8 b,,8 fs,8 ds8 fs8 ds'8 fs8 | % 43
   b,,8 gs,8 e8 gs8 b8 gs8 b,,8 fs,8 ds8 fs8 b8 fs8 | % 44
   b,,8 g,8 e8 b,8 fs8 ds'8 b,,8 g,8 e8 b,8 fs8 ds8 | % 45
   b,,8 fs,8 ds8 b8 r4 r2. | % 46
   <b, fs>2.\arpeggio <b,, fs, b,>2.\fermata\arpeggio | % 47
  \bar "|."
}

\score {
  \new PianoStaff \with { connectArpeggios = ##t } <<
    \new Staff = "up" \upper
    \new Staff = "down" \lower
  >>
  \layout {
    \context { \Score \override SpacingSpanner.common-shortest-duration = #(ly:make-moment 1/12) }
  }
}

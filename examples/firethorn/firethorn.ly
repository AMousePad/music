\version "2.24.0"
\language "english"
#(set-global-staff-size 18)
\header {
  title = "Firethorn"
  subtitle = "Rhapsodie-Étude in F-sharp minor"
  composer = "Claude, 2026"
  poet = "for piano solo"
  tagline = ##f
}
\paper {
  #(set-paper-size "a4")
  top-margin = 12\mm  bottom-margin = 12\mm  left-margin = 12\mm  right-margin = 12\mm
  system-system-spacing.basic-distance = #17
  ragged-last-bottom = ##f
}
upper = {
  \clef treble \time 2/4
  \override TupletBracket.bracket-visibility = ##f
  \set Staff.ottavationMarkups = #ottavation-simple-ordinals
  \key fs \minor \tempo "Lento a capriccio" 4 = 48 <fs fs'>4\f^\markup\italic"pesante" <cs' cs''>4 | % Intro 1
  <b b'>8. <a a'>16 <gs gs'>8. <a a'>16 | % Intro 2
  <cs' cs''>16 <bs bs'>16 <cs' cs''>8~ <cs' cs''>4 | % Intro 3
  r8 \ottava #1 cs''''8\pp^\markup\italic"quasi campanella" r8 cs''''8 | % Intro 4
  \ottava #0 <es es'>4\f <b b'>4 | % Intro 5
  <a a'>8. <gs gs'>16 <fs fs'>8. <gs gs'>16 | % Intro 6
  <b b'>16 <as as'>16 <b b'>8~ <b b'>4 | % Intro 7
  r8 \ottava #1 cs''''8\pp r8 cs''''8 | % Intro 8
  \ottava #0 d''4\p^\markup\italic"espressivo" a''4 | % Intro 9
  g''8 fs''8 e''8 fs''8 | % Intro 10
  a''8. gs''16 fs''4 | % Intro 11
  es''8\mp r8 a'64^\markup\italic"accelerando" bs' cs'' d'' es'' fs'' gs'' a'' bs'' cs''' d''' es''' fs''' gs''' a''' bs''' | % Intro 12
  \ottava #1 cs''''2\pp\fermata \bar "||" | % Intro 13
  \tempo "Tema.  Allegretto capriccioso" 4 = 96 \ottava #0 fs''8-.\p^\markup\italic"leggiero" cs'''8-. b''16 a''16 gs''16 a''16 | % Theme 1
  cs'''16 bs''16 cs'''8-. fs''8-. \ottava #1 cs''''8 | % Theme 2
  \ottava #0 es''8-. b''8-. a''16 gs''16 fs''16 gs''16 | % Theme 3
  b''16 as''16 b''8-. es''8-. \ottava #1 cs''''8 | % Theme 4
  \ottava #0 fs''8-. d'''8-. cs'''16 b''16 a''16 b''16 | % Theme 5
  b''16 as''16 b''8-. gs''8-. d'''8-. | % Theme 6
  cs'''8-. e'''8-. ds'''16 cs'''16 bs''16 a''16 | % Theme 7
  gs''8-. cs'''8-. es''8-. \ottava #1 cs''''8 | % Theme 8
  \ottava #0 fs''8-. cs'''8-. b''16 a''16 gs''16 a''16 | % Theme 9
  cs'''16 bs''16 cs'''8-. as''8-. e'''8-. | % Theme 10
  d'''8-.\mp fs'''8-. e'''16 d'''16 cs'''16 d'''16 | % Theme 11
  d'''16 cs'''16 d'''8-. b''8-. g''8-. | % Theme 12
  fs''8-.\> cs'''8-. b''16 a''16 gs''16 fs''16 | % Theme 13
  gs''16 fss''16 gs''8-. b''8-. es''8-. | % Theme 14
  fs''8-. a''8-. cs'''8-. fs'''8-. | % Theme 15
  cs'''16\p bs''16 cs'''8-. fs''8-. \ottava #1 cs''''8 \bar "||" | % Theme 16
  \tempo "Var. 1.  Presto" 4 = 152 r4 \ottava #0 cs'16\mp^\markup\italic"leggiero, non legato" fs'16 a'16 cs''16 | % Var1 1
  fs''16 cs'''16 b''16 a''16 gs''16 fs''16 es''16 fs''16 | % Var1 2
  r4 cs'16 es'16 gs'16 b'16 | % Var1 3
  es''16 b''16 a''16 gs''16 fs''16 es''16 ds''16 es''16 | % Var1 4
  r4 fs'16 a'16 d''16 fs''16 | % Var1 5
  gs''16 d'''16 cs'''16 b''16 a''16 gs''16 fs''16 gs''16 | % Var1 6
  r4 fs'16 a'16 bs'16 ds''16 | % Var1 7
  es''16 gs''16 fs''16 es''16 ds''16 cs''16 bs'16 cs''16 | % Var1 8
  fs''16\mf^\markup\italic"cresc." cs''16 cs'''16 a''16 b''16 a''16 gs''16 a''16 | % Var1 9
  cs'''16 bs''16 cs'''16 fs''16 as''16 fs''16 e'''16 cs'''16 | % Var1 10
  d'''16 b''16 fs'''16 d'''16 e'''16 d'''16 cs'''16 d'''16 | % Var1 11
  d'''16 cs'''16 d'''16 g''16 b''16 d''16 g''16 b'16 | % Var1 12
  fs''16\f cs''16 cs'''16 a''16 b''16 a''16 gs''16 fs''16 | % Var1 13
  gs''16 fss''16 gs''16 es''16 b''16 es''16 gs''16 es''16 | % Var1 14
  fs''16 cs''16 a''16 fs''16 cs'''16 a''16 fs'''16 cs'''16 | % Var1 15
  cs'''16 bs''16 cs'''16 a''16 fs''16 cs''16 a'16 fs'16 \bar "||" | % Var1 16
  \tempo "Var. 2.  L'istesso tempo" <a' cs'' fs''>8\f^\markup\italic"marcato il tema" <fs'' a'' cs'''>8 b''16 a''16 gs''16 a''16 | % Var2 1
  cs'''16 bs''16 cs'''8 <a' cs'' fs''>8 r8 | % Var2 2
  <gs' b' es''>8 <es'' gs'' b''>8 a''16 gs''16 fs''16 gs''16 | % Var2 3
  b''16 as''16 b''8 <gs' b' es''>8 r8 | % Var2 4
  <a' d'' fs''>8 <fs'' a'' d'''>8 cs'''16 b''16 a''16 b''16 | % Var2 5
  b''16 as''16 b''8 <b' d'' gs''>8 <e'' gs'' d'''>8 | % Var2 6
  <e'' a'' cs'''>8 <a'' cs''' e'''>8 ds'''16 cs'''16 bs''16 a''16 | % Var2 7
  <b' es'' gs''>8 <es'' gs'' cs'''>8 <gs' b' es''>8 r8 | % Var2 8
  <a' cs'' fs''>8 <fs'' a'' cs'''>8 b''16 a''16 gs''16 a''16 | % Var2 9
  cs'''16 bs''16 cs'''8 <cs'' e'' as''>8 <as'' cs''' e'''>8 | % Var2 10
  <fs'' b'' d'''>8 <b'' d''' fs'''>8 e'''16 d'''16 cs'''16 d'''16 | % Var2 11
  d'''16 cs'''16 d'''8 <d'' g'' b''>8 <b' d'' g''>8 | % Var2 12
  <a' cs'' fs''>8\ff <fs'' a'' cs'''>8 b''16 a''16 gs''16 fs''16 | % Var2 13
  gs''16 fss''16 gs''8 <es'' gs'' b''>8 <gs' b' es''>8 | % Var2 14
  <a' cs'' fs''>8 <cs'' fs'' a''>8 <fs'' a'' cs'''>8 <a'' cs''' fs'''>8 | % Var2 15
  cs'''16 bs''16 cs'''8 <a' cs'' fs''>8 r8 \bar "||" | % Var2 16
  \tempo "Var. 3.  Allegretto" 4 = 108 \ottava #1 fs''16\pp^\markup\italic"leggierissimo" cs''''16 cs'''16 cs''''16 b''16 cs''''16 a''16 cs''''16 | % Var3 1
  cs'''16 cs''''16 bs''16 cs''''16 cs'''16 cs''''16 fs''16 cs''''16 | % Var3 2
  es''16 cs''''16 b''16 cs''''16 a''16 cs''''16 gs''16 cs''''16 | % Var3 3
  b''16 cs''''16 as''16 cs''''16 b''16 cs''''16 es''16 cs''''16 | % Var3 4
  fs''16 d''''16 d'''16 d''''16 cs'''16 d''''16 b''16 d''''16 | % Var3 5
  b''16 d''''16 as''16 d''''16 b''16 d''''16 gs''16 d''''16 | % Var3 6
  cs'''16 cs''''16 e'''16 cs''''16 ds'''16 ds''''16 bs''16 ds''''16 | % Var3 7
  gs''16 cs''''16 cs'''16 cs''''16 es''16 cs''''16 gs''16 cs''''16 | % Var3 8
  fs''16\p cs''''16 cs'''16 cs''''16 a'''32 gs'''32 g'''32 fs'''32 f'''32 e'''32 ds'''32 d'''32 | % Var3 9
  cs'''16 cs''''16 as''16 cs''''16 fs''32 g''32 gs''32 a''32 as''32 b''32 c'''32 cs'''32 | % Var3 10
  d'''16 d''''16 fs'''16 d''''16 as'''32 a'''32 gs'''32 g'''32 fs'''32 f'''32 e'''32 ds'''32 | % Var3 11
  d'''16 d''''16 b''16 d''''16 d'''32 cs'''32 c'''32 b''32 as''32 a''32 gs''32 g''32 | % Var3 12
  fs''16\> cs''''16 cs'''16 cs''''16 e'''32 ds'''32 d'''32 cs'''32 c'''32 b''32 as''32 a''32 | % Var3 13
  gs''16 cs''''16 b''16 cs''''16 d'''32 cs'''32 c'''32 b''32 as''32 a''32 gs''32 g''32 | % Var3 14
  fs''16 cs''''16 cs'''16 cs''''16 cs'''32 d'''32 ds'''32 e'''32 es'''32 fs'''32 g'''32 gs'''32 | % Var3 15
  a'''16\pp cs''''16 fs'''16 cs''''16 cs'''16 cs''''16 fs''16 cs''''16 \bar "||" | % Var3 16
  \tempo "Var. 4.  Meno mosso" 4 = 78 \ottava #0 \tuplet 3/2 { fs''16\p^\markup\italic"non legato" fs'' fs'' } \tuplet 3/2 { cs'''16 cs''' cs''' } b''16 a''16 gs''16 a''16 | % Var4 1
  cs'''16 bs''16 \tuplet 3/2 { cs'''16 cs''' cs''' } \tuplet 3/2 { fs''16 fs'' fs'' } \ottava #1 cs''''8 | % Var4 2
  \ottava #0 \tuplet 3/2 { es''16 es'' es'' } \tuplet 3/2 { b''16 b'' b'' } a''16 gs''16 fs''16 gs''16 | % Var4 3
  b''16 as''16 \tuplet 3/2 { b''16 b'' b'' } \tuplet 3/2 { es''16 es'' es'' } \ottava #1 cs''''8 | % Var4 4
  \ottava #0 \tuplet 3/2 { fs''16 fs'' fs'' } \tuplet 3/2 { d'''16 d''' d''' } cs'''16 b''16 a''16 b''16 | % Var4 5
  b''16 as''16 \tuplet 3/2 { b''16 b'' b'' } \tuplet 3/2 { gs''16 gs'' gs'' } \tuplet 3/2 { d'''16 d''' d''' } | % Var4 6
  \tuplet 3/2 { cs'''16 cs''' cs''' } \tuplet 3/2 { e'''16 e''' e''' } ds'''16 cs'''16 bs''16 a''16 | % Var4 7
  \tuplet 3/2 { gs''16 gs'' gs'' } \tuplet 3/2 { cs'''16 cs''' cs''' } \tuplet 3/2 { es''16 es'' es'' } \ottava #1 cs''''8 | % Var4 8
  \ottava #0 fs''32\mp\< fs''32 fs''32 fs''32 cs'''32 cs'''32 cs'''32 cs'''32 b''32 b''32 a''32 a''32 gs''32 gs''32 a''32 a''32 | % Var4 9
  cs'''32 cs'''32 bs''32 bs''32 cs'''32 cs'''32 cs'''32 cs'''32 as''32 as''32 as''32 as''32 e'''32 e'''32 e'''32 e'''32 | % Var4 10
  d'''32 d'''32 d'''32 d'''32 fs'''32 fs'''32 fs'''32 fs'''32 e'''32 e'''32 d'''32 d'''32 cs'''32 cs'''32 d'''32 d'''32 | % Var4 11
  d'''32 d'''32 cs'''32 cs'''32 d'''32 d'''32 d'''32 d'''32 b''32 b''32 b''32 b''32 g''32 g''32 g''32 g''32 | % Var4 12
  fs''32\mf\> fs''32 fs''32 fs''32 cs'''32 cs'''32 cs'''32 cs'''32 b''32 b''32 a''32 a''32 gs''32 gs''32 fs''32 fs''32 | % Var4 13
  gs''32 gs''32 fss''32 fss''32 gs''32 gs''32 gs''32 gs''32 b''32 b''32 b''32 b''32 es''32 es''32 es''32 es''32 | % Var4 14
  fs''32 fs''32 fs''32 fs''32 a''32 a''32 a''32 a''32 cs'''32 cs'''32 cs'''32 cs'''32 fs'''32 fs'''32 fs'''32 fs'''32 | % Var4 15
  cs'''32\p cs'''32 bs''32 bs''32 cs'''32 cs'''32 cs'''32 cs'''32 fs''32 fs''32 fs''16 \ottava #1 cs''''8 \bar "||" | % Var4 16
  cs''''8\pp^\markup\italic"ritenuto" r8 cs''''8 r8 | % Trans 1
  cs''''4 d''''4 \bar "||" | % Trans 2
  \key d \major \tempo "Andante cantabile" 4 = 56 << { \voiceOne \ottava #0 r32 fs'32\pp^\markup\italic"dolcissimo" a'32 d''32 fs''32 d''32 a'32 fs'32 r32 d''32 fs''32 a''32 d'''32 a''32 fs''32 d''32 } \new Voice { \voiceTwo d'4_\markup\italic"il canto ben marcato" a'4 } >> \oneVoice | % Middle 1
  << { \voiceOne r32 b'32 d''32 b'32 r32 b'32 d''32 b'32 r32 a'32 d''32 a'32 r32 a'32 d''32 a'32 } \new Voice { \voiceTwo g'8 fs'8 e'8 fs'8 } >> \oneVoice | % Middle 2
  << { \voiceOne r32 cs''32 e''32 cs''32 r32 cs''32 e''32 cs''32 r32 cs''32 e''32 g''32 cs'''32 g''32 e''32 cs''32 } \new Voice { \voiceTwo a'8 gs'8 a'4 } >> \oneVoice | % Middle 3
  << { \voiceOne r32 fs'32 a'32 d''32 fs''32 d''32 a'32 fs'32 fs'32 a'32 d''32 fs''32 a''32 fs''32 d''32 a'32 } \new Voice { \voiceTwo d'2 } >> \oneVoice | % Middle 4
  << { \voiceOne r32 g'32 b'32 e''32 g''32 e''32 b'32 g'32 r32 e''32 g''32 b''32 e'''32 b''32 g''32 e''32 } \new Voice { \voiceTwo e'4 b'4 } >> \oneVoice | % Middle 5
  << { \voiceOne r32 e''32 g''32 e''32 r32 b'32 e''32 b'32 r32 a'32 cs''32 a'32 r32 g'32 cs''32 g'32 } \new Voice { \voiceTwo a'8 g'8 fs'8 e'8 } >> \oneVoice | % Middle 6
  << { \voiceOne r32 d''32 fs''32 d''32 r32 d''32 fs''32 d''32 r32 d''32 fs''32 b''32 d'''32 b''32 fs''32 d''32 } \new Voice { \voiceTwo b'8 as'8 b'4 } >> \oneVoice | % Middle 7
  << { \voiceOne r32 gs'32 b'32 d''32 gs''32 d''32 b'32 gs'32 a'32 cs''32 e''32 a''32 cs'''32 a''32 e''32 cs''32 } \new Voice { \voiceTwo e'2 } >> \oneVoice | % Middle 8
  <d' fs' d''>4\mf^\markup\italic"con anima" <a' d'' a''>4 | % Middle 9
  <g' g''>8 <fs' fs''>8 <e' e''>8 <fs' fs''>8 | % Middle 10
  <a' a''>8 <gs' gs''>8 <a' cs'' a''>4 | % Middle 11
  <d'' fs'' d'''>2 | % Middle 12
  <g' b' g''>4 <d'' g'' d'''>4 | % Middle 13
  <c'' c'''>8 <bf' bf''>8 <a' a''>8 <bf' bf''>8 | % Middle 14
  <a' d'' a''>4\< <fs'' a'' fs'''>4 | % Middle 15
  <e'' g'' e'''>4 <cs'' g'' cs'''>4 | % Middle 16
  \tempo "Largamente" 4 = 54 <d'' fs'' a'' d'''>4\ff^\markup\italic"grandioso" \ottava #1 <a'' d''' fs''' a'''>4 | % Middle 17
  <g'' b'' d''' g'''>8 <fs'' fs'''>8 <e'' e'''>8 <fs'' a'' d''' fs'''>8 | % Middle 18
  <fs'' as'' cs''' fs'''>4 <cs''' fs''' as''' cs''''>4 | % Middle 19
  <b'' ds''' fs''' b'''>8 <as'' as'''>8 <gs'' gs'''>8 <as'' cs''' fs''' as'''>8 | % Middle 20
  \ottava #0 <bf' d'' f'' bf''>4\> <f'' bf'' d''' f'''>4 | % Middle 21
  <ef'' g'' bf'' ef'''>8 <d'' d'''>8 <c'' c'''>8 <d'' f'' bf'' d'''>8 | % Middle 22
  <fs'' a'' bs''>2\p^\markup\italic"ritardando" | % Middle 23
  <es'' gs'' b'' cs'''>2\pp\fermata \bar "||" | % Middle 24
  \key fs \minor \tempo "Poco a poco accelerando" r4 gs''16\pp fss''16 gs''8 | % Retrans 1
  r4 b''16 as''16 b''8 | % Retrans 2
  es'''16 dss'''16 es'''8 gs'''16 fss'''16 gs'''8 | % Retrans 3
  \ottava #1 cs''''32\mf\< bs'''32 a'''32 gs'''32 fs'''32 es'''32 d'''32 cs'''32 bs''32 a''32 gs''32 fs''32 es''32 d''32 cs''32 bs'32 | % Retrans 4
  \ottava #0 a'32 gs'32 fs'32 es'32 d'32 cs'32 bs32 r32 r4 | % Retrans 5
  cs''16\f\< es''16 gs''16 cs'''16 es'''16 gs'''16 \ottava #1 cs''''8 \bar "||" | % Retrans 6
  \tempo "Var. 5.  Presto con fuoco" 4 = 132 \ottava #0 <fs' fs''>8\ff^\markup\italic"marcatissimo" <cs'' cs'''>8 <b' b''>16 <a' a''>16 <gs' gs''>16 <a' a''>16 | % Var5 1
  <cs'' cs'''>16 <bs' bs''>16 <cs'' cs'''>8 <fs' fs''>8 r8 | % Var5 2
  <es' es''>8 <b' b''>8 <a' a''>16 <gs' gs''>16 <fs' fs''>16 <gs' gs''>16 | % Var5 3
  <b' b''>16 <as' as''>16 <b' b''>8 <es' es''>8 r8 | % Var5 4
  <fs' fs''>8 <d'' d'''>8 <cs'' cs'''>16 <b' b''>16 <a' a''>16 <b' b''>16 | % Var5 5
  <b' b''>16 <as' as''>16 <b' b''>8 <gs' gs''>8 <d'' d'''>8 | % Var5 6
  <cs'' cs'''>8 <e'' e'''>8 <ds'' ds'''>16 <cs'' cs'''>16 <bs' bs''>16 <a' a''>16 | % Var5 7
  <gs' gs''>8 <cs'' cs'''>8 <es' es''>8 r8 | % Var5 8
  \ottava #1 <fs'' fs'''>8^\markup\italic"con fuoco" <cs''' cs''''>8 <b'' b'''>16 <a'' a'''>16 <gs'' gs'''>16 <a'' a'''>16 | % Var5 9
  <cs''' cs''''>16 <bs'' bs'''>16 <cs''' cs''''>8 <as'' as'''>8 <e''' e''''>8 | % Var5 10
  <d''' d''''>8 <fs''' fs''''>8 <e''' e''''>16 <d''' d''''>16 <cs''' cs''''>16 <d''' d''''>16 | % Var5 11
  <d''' d''''>16 <cs''' cs''''>16 <d''' d''''>8 <b'' b'''>8 <g'' g'''>8 | % Var5 12
  <fs'' fs'''>8 <cs''' cs''''>8 <b'' b'''>16 <a'' a'''>16 <gs'' gs'''>16 <fs'' fs'''>16 | % Var5 13
  <gs'' gs'''>16 <fss'' fss'''>16 <gs'' gs'''>8 <b'' b'''>8 <es'' es'''>8 | % Var5 14
  <fs'' fs'''>8 <a'' a'''>8 <cs''' cs''''>8 <fs''' fs''''>8 | % Var5 15
  <cs''' cs''''>16 <bs'' bs'''>16 <cs''' cs''''>8 <a'' cs''' fs'''>8 r8 \bar "||" | % Var5 16
  \key fs \major \tempo "Coda.  Vivace" 4 = 146 \ottava #0 \acciaccatura es''8 fs''8-.\p^\markup\italic"scherzando" cs'''8-. b''16 as''16 gs''16 as''16 | % Coda 1
  cs'''16 bs''16 cs'''8-. fs''8-. \ottava #1 cs''''8 | % Coda 2
  \ottava #0 \acciaccatura dss''8 es''8-. b''8-. as''16 gs''16 fs''16 gs''16 | % Coda 3
  b''16 as''16 b''8-. es''8-. \ottava #1 cs''''8 | % Coda 4
  \ottava #0 \acciaccatura es''8 fs''8-. ds'''8-. cs'''16 b''16 as''16 b''16 | % Coda 5
  b''16 as''16 b''8-. gs''8-. ds'''8-. | % Coda 6
  cs'''8-. as''8-. gs''16 fs''16 es''16 gs''16 | % Coda 7
  fs''8-. as''8-. cs'''8-. \ottava #1 cs''''8 | % Coda 8
  \tuplet 6/4 { fs''16\mp^\markup\italic"leggiero, crescendo" as'' cs''' fs''' as''' cs'''' } \tuplet 6/4 { b'''16 as''' gs''' as''' fs''' ds''' } | % Coda 9
  \tuplet 6/4 { cs'''16 bs'' cs''' fs''' cs''' as'' } \tuplet 6/4 { fs''16 as'' cs''' as'' fs'' cs'' } | % Coda 10
  \tuplet 6/4 { es''16 gs'' b'' es''' gs''' b''' } \tuplet 6/4 { as'''16 gs''' fs''' gs''' es''' cs''' } | % Coda 11
  \tuplet 6/4 { b''16 as'' b'' es''' b'' gs'' } \tuplet 6/4 { es''16 gs'' b'' cs''' es''' cs''' } | % Coda 12
  \tuplet 6/4 { ds'''16 fs''' b''' fs''' ds''' b'' } \tuplet 6/4 { es'''16 ds''' cs''' ds''' b'' fs'' } | % Coda 13
  \tuplet 6/4 { d'''16 cs''' d''' fs''' d''' bs'' } \tuplet 6/4 { a''16 bs'' d''' bs'' a'' fs'' } | % Coda 14
  \tuplet 6/4 { as''16 cs''' fs''' as''' cs'''' as''' } \tuplet 6/4 { b'''16 gs''' es''' b'' gs'' es'' } | % Coda 15
  \tuplet 6/4 { fs''16 as'' cs''' fs''' as''' cs'''' } fs'''8 cs''''8 | % Coda 16
  \tempo "Più mosso" 4 = 152 <fs'' fs'''>8\ff^\markup\italic"con bravura" <cs''' cs''''>8 <b'' b'''>16 <as'' as'''>16 <gs'' gs'''>16 <as'' as'''>16 | % Coda 17
  <cs''' cs''''>16 <bs'' bs'''>16 <cs''' cs''''>8 <fs'' fs'''>8 <cs''' cs''''>8 | % Coda 18
  <es'' es'''>8 <b'' b'''>8 <as'' as'''>16 <gs'' gs'''>16 <fs'' fs'''>16 <gs'' gs'''>16 | % Coda 19
  <b'' b'''>16 <as'' as'''>16 <b'' b'''>8 <es'' es'''>8 <cs''' cs''''>8 | % Coda 20
  <fs'' fs'''>8 <ds''' ds''''>8 <cs''' cs''''>16 <b'' b'''>16 <as'' as'''>16 <b'' b'''>16 | % Coda 21
  <b'' b'''>16 <as'' as'''>16 <b'' b'''>8 <gs'' gs'''>8 <ds''' ds''''>8 | % Coda 22
  <cs''' cs''''>8 <as'' as'''>8 <gs'' gs'''>16 <fs'' fs'''>16 <es'' es'''>16 <gs'' gs'''>16 | % Coda 23
  <fs'' fs'''>8 <as'' as'''>8 <cs''' cs''''>8 <cs''' cs''''>8 | % Coda 24
  <fs'' fs'''>8 <cs''' cs''''>8 <b'' b'''>16 <as'' as'''>16 <gs'' gs'''>16 <as'' as'''>16 | % Coda 25
  <cs''' cs''''>16 <bs'' bs'''>16 <cs''' cs''''>8 <fs'' fs'''>8 <cs''' cs''''>8 | % Coda 26
  <es'' es'''>8 <b'' b'''>8 <as'' as'''>16 <gs'' gs'''>16 <fs'' fs'''>16 <gs'' gs'''>16 | % Coda 27
  <b'' b'''>16 <as'' as'''>16 <b'' b'''>8 <es'' es'''>8 <cs''' cs''''>8 | % Coda 28
  <ds''' ds''''>8 <fs''' fs''''>8 <es''' es''''>16 <ds''' ds''''>16 <cs''' cs''''>16 <ds''' ds''''>16 | % Coda 29
  <d''' d''''>16 <cs''' cs''''>16 <d''' d''''>8 <bs'' bs'''>8 <a'' a'''>8 | % Coda 30
  <as'' as'''>8 <fs'' fs'''>8 <as'' as'''>8 <cs''' cs''''>8 | % Coda 31
  <es''' es''''>8 <cs''' cs''''>8 <b'' b'''>8 <gs'' gs'''>8 | % Coda 32
  \tempo "Martellato" 4 = 132 \clef bass r32 \ottava #0 <cs cs'>32\f\< r32 <ds ds'>32 r32 <es es'>32 r32 <fss fss'>32 \clef treble r32 <a a'>32 r32 <b b'>32 r32 <cs' cs''>32 r32 <ds' ds''>32 | % Coda 33
  r32 <es' es''>32 r32 <fss' fss''>32 r32 <a' a''>32 r32 <b' b''>32 r32 <cs'' cs'''>32 r32 <ds'' ds'''>32 r32 <es'' es'''>32 r16 | % Coda 34
  \ottava #1 <as'' cs''' fs'''>4\fff <es''' es''''>32 r32 <cs''' cs''''>32 r32 <as'' as'''>32 r32 <fs'' fs'''>32 r32 | % Coda 35
  \ottava #0 <ds'' ds'''>32 r32 <b' b''>32 r32 <gs' gs''>32 r32 <es' es''>32 r32 <cs' cs''>32 r32 <as as'>32 r32 <fs fs'>32 r32 r16 | % Coda 36
  r32 <fs' b' ds''>32 r32 <fs' b' ds''>32 r32 <b' ds'' fs''>32 r32 <b' ds'' fs''>32 r32 <fs' a' bs'>32 r32 <fs' a' bs'>32 r32 <fs' a' bs'>32 r32 <fs' a' bs'>32 | % Coda 37
  r32 <fs' as' cs''>32 r32 <fs' as' cs''>32 r32 <as' cs'' fs''>32 r32 <as' cs'' fs''>32 r32 <cs'' fs'' as''>32 r32 <cs'' fs'' as''>32 r32 <fs'' as'' cs'''>32 r32 <fs'' as'' cs'''>32 | % Coda 38
  r32 <gs' b' es''>32 r32 <gs' b' es''>32 r32 <b' es'' gs''>32 r32 <b' es'' gs''>32 r32 <es'' gs'' b''>32 r32 <es'' gs'' b''>32 r32 <gs'' b'' es'''>32 r16 | % Coda 39
  <gs'' b'' es''' gs'''>8 <gs'' b'' es''' gs'''>8 <gs'' b'' es''' gs'''>8 r8 | % Coda 40
  <as'' cs''' fs'''>8\fff cs''16 fs''16 as''16 cs'''16 fs'''16 \ottava #1 as'''16 | % Coda 41
  <fs''' as''' cs''''>8 r8 <as'' cs''' fs'''>8 r8 | % Coda 42
  \tempo "Largamente" 4 = 88 <gs'' b'' cs''' es'''>4 <fs'' as'' cs''' fs'''>4 | % Coda 43
  \ottava #0 <fs' as' cs'' fs''>2\fermata \bar "|." | % Coda 44
}
lower = {
  \clef bass \time 2/4
  \override TupletBracket.bracket-visibility = ##f
  \set Staff.ottavationMarkups = #ottavation-simple-ordinals
  \key fs \minor <fs,, fs,>4_\markup\italic"con Ped." <cs, cs>4 | % Intro 1
  <b,, b,>8. <a,, a,>16 <gs,, gs,>8. <a,, a,>16 | % Intro 2
  <cs, cs>16 <bs,, bs,>16 <cs, cs>8~ <cs, cs>4 | % Intro 3
  R2 | % Intro 4
  <es,, es,>4 <b,, b,>4 | % Intro 5
  <a,, a,>8. <gs,, gs,>16 <fs,, fs,>8. <gs,, gs,>16 | % Intro 6
  <b,, b,>16 <as,, as,>16 <b,, b,>8~ <b,, b,>4 | % Intro 7
  R2 | % Intro 8
  <d, d>8 <fs a d'>8~ <fs a d'>4 | % Intro 9
  <d, d>8 <fs a bs>8~ <fs a bs>4 | % Intro 10
  <cs, cs>8 <fs a cs'>8~ <fs a cs'>4 | % Intro 11
  <cs, cs>8 gs64 a bs cs' d' es' fs' gs' r4 | % Intro 12
  R2\fermata \bar "||" | % Intro 13
  fs,8-._\markup\italic"a touch of pedal with each bass note" <fs a cs'>8-. r8 <fs a cs'>8-. | % Theme 1
  fs,8-. <fs a cs'>8-. r4 | % Theme 2
  cs8-. <es gs b>8-. r8 <es gs b>8-. | % Theme 3
  cs8-. <es gs b>8-. r4 | % Theme 4
  d8-. <fs a d'>8-. r8 <fs a d'>8-. | % Theme 5
  e,8-. <e gs d'>8-. r8 <e gs d'>8-. | % Theme 6
  a,8-. <e a cs'>8-. bs,8-. <ds fs a>8-. | % Theme 7
  cs8-. <es gs b>8-. cs,8-. r8 | % Theme 8
  fs,8-. <fs a cs'>8-. r8 <fs a cs'>8-. | % Theme 9
  as,8-. <e fs cs'>8-. r8 <e fs cs'>8-. | % Theme 10
  b,8-. <fs b d'>8-. r8 <fs b d'>8-. | % Theme 11
  b,8-. <g b d'>8-. r8 <g b d'>8-. | % Theme 12
  cs8-. <fs a cs'>8-. r8 <fs a cs'>8-. | % Theme 13
  cs8-. <es gs b>8-. cs,8-. <es gs b>8-. | % Theme 14
  fs,8-. <fs a cs'>8-. r8 <fs a cs'>8-. | % Theme 15
  fs,8-. <fs a cs'>8-. r4 \bar "||" | % Theme 16
  fs,16_\markup\italic"senza Ped." cs16 fs16 a16 r4 | % Var1 1
  R2 | % Var1 2
  cs16 es16 gs16 b16 r4 | % Var1 3
  R2 | % Var1 4
  d16 fs16 a16 d'16 r4 | % Var1 5
  R2 | % Var1 6
  a,16 e16 a16 cs'16 r4 | % Var1 7
  r4 cs8 cs,8 | % Var1 8
  fs,8-._\markup\italic"poco Ped." <fs a cs'>8-. cs8-. <fs a cs'>8-. | % Var1 9
  as,8-. <e fs cs'>8-. fs,8-. <e fs cs'>8-. | % Var1 10
  b,8-. <fs b d'>8-. fs,8-. <fs b d'>8-. | % Var1 11
  b,8-. <g b d'>8-. g,8-. <g b d'>8-. | % Var1 12
  cs8-. <fs a cs'>8-. cs,8-. <fs a cs'>8-. | % Var1 13
  cs8-. <es gs b>8-. cs,8-. <es gs b>8-. | % Var1 14
  fs,8-. <fs a cs'>8-. a,8-. <fs a cs'>8-. | % Var1 15
  fs,8-. <fs a cs'>8-. fs,8-. r8 \bar "||" | % Var1 16
  fs,16 cs16 fs16 gs16 a16 gs16 fs16 cs16 | % Var2 1
  fs,16 cs16 fs16 a16 cs'16 a16 fs16 cs16 | % Var2 2
  cs,16 gs,16 b,16 cs16 es16 cs16 b,16 gs,16 | % Var2 3
  cs,16 gs,16 cs16 es16 gs16 es16 cs16 gs,16 | % Var2 4
  d,16 a,16 d16 e16 fs16 e16 d16 a,16 | % Var2 5
  e,16 b,16 d16 e16 gs16 e16 d16 b,16 | % Var2 6
  a,16 e16 a16 e16 bs,16 fs16 a16 fs16 | % Var2 7
  cs16 gs16 es16 cs16 b,16 gs,16 es,16 cs,16 | % Var2 8
  fs,16 cs16 a16 cs'16 fs'16 cs'16 a16 cs16 | % Var2 9
  as,16 fs16 cs'16 e'16 fs'16 e'16 cs'16 fs16 | % Var2 10
  b,16 fs16 d'16 fs'16 b'16 fs'16 d'16 fs16 | % Var2 11
  b,16 g16 d'16 g'16 b'16 g'16 d'16 g16 | % Var2 12
  cs16 a16 cs'16 fs'16 a'16 fs'16 cs'16 a16 | % Var2 13
  cs16 gs16 b16 es'16 gs'16 es'16 b16 gs16 | % Var2 14
  fs,16 cs16 fs16 a16 \clef treble cs'16 fs'16 a'16 cs''16 | % Var2 15
  \clef bass fs'16 cs'16 a16 fs16 <fs, fs>8 r8 \bar "||" | % Var2 16
  fs,8-._\markup\italic"una corda" <fs a cs'>8-. r8 <fs a cs'>8-. | % Var3 1
  fs,8-. <fs a cs'>8-. r4 | % Var3 2
  cs8-. <es gs b>8-. r8 <es gs b>8-. | % Var3 3
  cs8-. <es gs b>8-. r4 | % Var3 4
  d8-. <fs a d'>8-. r8 <fs a d'>8-. | % Var3 5
  e,8-. <e gs d'>8-. r8 <e gs d'>8-. | % Var3 6
  a,8-. <e a cs'>8-. bs,8-. <ds fs a>8-. | % Var3 7
  cs8-. <es gs b>8-. cs,8-. r8 | % Var3 8
  fs,8-._\markup\italic"tre corde" <fs a cs'>8-. r8 <fs a cs'>8-. | % Var3 9
  as,8-. <e fs cs'>8-. r8 <e fs cs'>8-. | % Var3 10
  b,8-. <fs b d'>8-. r8 <fs b d'>8-. | % Var3 11
  b,8-. <g b d'>8-. r8 <g b d'>8-. | % Var3 12
  cs8-. <fs a cs'>8-. r8 <fs a cs'>8-. | % Var3 13
  cs8-. <es gs b>8-. cs,8-. <es gs b>8-. | % Var3 14
  fs,8-. <fs a cs'>8-. r8 <fs a cs'>8-. | % Var3 15
  fs,8-. <fs a cs'>8-. r4 \bar "||" | % Var3 16
  fs,8-. cs8-. a8-. cs8-. | % Var4 1
  fs,8-. cs8-. a8-. r8 | % Var4 2
  cs,8-. gs,8-. es8-. b,8-. | % Var4 3
  cs,8-. gs,8-. es8-. r8 | % Var4 4
  d,8-. a,8-. fs8-. a,8-. | % Var4 5
  e,8-. b,8-. gs8-. d8-. | % Var4 6
  a,8-. e8-. bs,8-. fs8-. | % Var4 7
  cs8-. gs,8-. cs,8-. r8 | % Var4 8
  fs,8-. cs8-. a8-. cs8-. | % Var4 9
  as,8-. fs8-. e8-. cs8-. | % Var4 10
  b,8-. fs8-. d'8-. fs8-. | % Var4 11
  b,8-. g8-. d'8-. g8-. | % Var4 12
  cs8-. a8-. fs8-. a8-. | % Var4 13
  cs8-. gs8-. b8-. es8-. | % Var4 14
  fs,8-. cs8-. a8-. cs8-. | % Var4 15
  fs,8-. cs8-. <fs a cs'>8-. r8 \bar "||" | % Var4 16
  fs,8_\markup\italic"una corda" <cs a>8~ <cs a>4 | % Trans 1
  fs,8 <d a>8~ <d a>4 \bar "||" | % Trans 2
  \key d \major d,16_\markup\italic"tre corde, con Ped." a,16 d16 fs16 a,16 d16 fs16 a16 | % Middle 1
  b,16 d16 g16 b16 a,16 d16 fs16 a16 | % Middle 2
  a,16 e16 g16 cs'16 a,16 e16 g16 cs'16 | % Middle 3
  fs,16 d16 fs16 a16 fs16 d16 fs16 a16 | % Middle 4
  e,16 b,16 e16 g16 b,16 e16 g16 b16 | % Middle 5
  g,16 e16 g16 b16 a,16 e16 g16 cs'16 | % Middle 6
  b,16 fs16 b16 d'16 b,16 fs16 b16 d'16 | % Middle 7
  gs,16 e16 b16 e16 a,16 e16 a16 cs'16 | % Middle 8
  \tuplet 6/4 { d,16 a, d fs a fs } \tuplet 6/4 { d16 a, d fs a fs } | % Middle 9
  \tuplet 6/4 { b,16 d g b d' b } \tuplet 6/4 { a,16 d fs a d' a } | % Middle 10
  \tuplet 6/4 { a,16 e g cs' e' cs' } \tuplet 6/4 { a16 e g cs' e' cs' } | % Middle 11
  \tuplet 6/4 { c16 fs a d' fs' d' } \tuplet 6/4 { a16 fs a d' fs' d' } | % Middle 12
  \tuplet 6/4 { b,16 g b d' b g } \tuplet 6/4 { b,16 g b d' b g } | % Middle 13
  \tuplet 6/4 { bf,16 g bf d' bf g } \tuplet 6/4 { bf,16 g bf d' bf g } | % Middle 14
  \tuplet 6/4 { a,16 fs a d' a fs } \tuplet 6/4 { a,16 fs a d' a fs } | % Middle 15
  \tuplet 6/4 { a,16 e g cs' g e } \tuplet 6/4 { a,16 e g cs' g e } | % Middle 16
  \ottava #-1 <d,, d,>32 \ottava #0 \tuplet 11/7 { a,32 d fs a d' fs' a' fs' d' a fs } \tuplet 11/7 { d32 a, d fs a d' fs' a' fs' d' a } r32 | % Middle 17
  <b,, b,>32 \tuplet 10/6 { g32 b d' g' b' g' d' b g d } r32 <a,, a,>32 \tuplet 10/6 { fs32 a d' fs' a' fs' d' a fs d } r32 | % Middle 18
  <fs,, fs,>32 \tuplet 11/7 { cs32 fs as cs' fs' as' cs'' as' fs' cs' as } \tuplet 11/7 { fs32 cs fs as cs' fs' as' cs'' as' fs' cs' } r32 | % Middle 19
  <ds, ds>32 \tuplet 10/6 { b32 ds' fs' b' ds'' b' fs' ds' b fs } r32 <cs, cs>32 \tuplet 10/6 { as32 cs' fs' as' cs'' as' fs' cs' as fs } r32 | % Middle 20
  <bf,, bf,>32 f32 bf32 d'32 f'32 d'32 bf32 f32 bf32 d'32 f'32 bf'32 f'32 d'32 bf32 r32 | % Middle 21
  <g,, g,>32 ef32 g32 bf32 ef'32 bf32 g32 r32 <f,, f,>32 d32 f32 bf32 d'32 bf32 f32 r32 | % Middle 22
  \ottava #-1 <d,, d,>32 \ottava #0 a,32 d32 fs32 a32 bs32 a32 fs32 d32 a,32 d32 fs32 a32 bs32 a32 r32 | % Middle 23
  \ottava #-1 <cs,, cs,>2\fermata \bar "||" | % Middle 24
  \key fs \minor \ottava #0 cs,16 cs16 cs,16 cs16 cs,16 cs16 cs,16 cs16 | % Retrans 1
  cs,16 cs16 cs,16 cs16 cs,16 cs16 cs,16 cs16 | % Retrans 2
  cs,16 cs16 cs,16 cs16 cs,16 cs16 cs,16 cs16 | % Retrans 3
  <cs, cs>8 <es gs b>8 r8 <es gs b>8 | % Retrans 4
  r8. r32 a32 gs32 fs32 es32 d32 cs32 bs,32 cs32 r32 | % Retrans 5
  <cs, cs>8 <es, es>8 <gs, gs>8 <cs, cs>8 \bar "||" | % Retrans 6
  <fs, fs>8 <cs cs'>8 <b, b>16 <a, a>16 <gs, gs>16 <a, a>16 | % Var5 1
  <cs cs'>16 <bs, bs>16 <cs cs'>8 <fs, fs>8 <fs,, fs,>8 | % Var5 2
  <es, es>8 <b, b>8 <a, a>16 <gs, gs>16 <fs, fs>16 <gs, gs>16 | % Var5 3
  <b, b>16 <as, as>16 <b, b>8 <es, es>8 \ottava #-1 <cs,, cs,>8 | % Var5 4
  \ottava #0 <fs, fs>8 <d d'>8 <cs cs'>16 <b, b>16 <a, a>16 <b, b>16 | % Var5 5
  <b, b>16 <as, as>16 <b, b>8 <gs, gs>8 <d d'>8 | % Var5 6
  <cs cs'>8 <e e'>8 <ds ds'>16 <cs cs'>16 <bs, bs>16 <a, a>16 | % Var5 7
  <gs, gs>8 <cs cs'>8 <es, es>8 \ottava #-1 <cs,, cs,>8 | % Var5 8
  \ottava #0 <fs,, fs,>8 <fs a cs'>8 <cs, cs>8 <fs a cs'>8 | % Var5 9
  <as,, as,>8 <e fs cs'>8 <fs, fs>8 <e fs cs'>8 | % Var5 10
  <b,, b,>8 <fs b d'>8 <fs, fs>8 <fs b d'>8 | % Var5 11
  <b,, b,>8 <g b d'>8 <g, g>8 <g b d'>8 | % Var5 12
  <cs, cs>8 <fs a cs'>8 <cs, cs>8 <fs a cs'>8 | % Var5 13
  <cs, cs>8 <es gs b>8 <cs, cs>8 <es gs b>8 | % Var5 14
  <fs,, fs,>8 <fs a cs'>8 <a,, a,>8 <fs a cs'>8 | % Var5 15
  <fs, fs>8 r8 <fs,, fs,>8 r8 \bar "||" | % Var5 16
  \key fs \major \grace s8 fs,8-. <as cs' fs'>8-. cs8-. <as cs' fs'>8-. | % Coda 1
  fs,8-. <as cs' fs'>8-. cs8-. r8 | % Coda 2
  \grace s8 cs8-. <es gs b>8-. gs,8-. <es gs b>8-. | % Coda 3
  cs8-. <es gs b>8-. gs,8-. r8 | % Coda 4
  \grace s8 b,8-. <fs b ds'>8-. fs,8-. <fs b ds'>8-. | % Coda 5
  gs,8-. <gs b ds'>8-. ds8-. <gs b ds'>8-. | % Coda 6
  cs8-. <fs as cs'>8-. cs8-. <es gs b>8-. | % Coda 7
  fs,8-. <as cs' fs'>8-. fs,8-. r8 | % Coda 8
  fs,8-. <as cs' fs'>8-. cs8-. <as cs' fs'>8-. | % Coda 9
  fs,8-. <as cs' fs'>8-. cs8-. r8 | % Coda 10
  cs8-. <es gs b>8-. gs,8-. <es gs b>8-. | % Coda 11
  cs8-. <es gs b>8-. gs,8-. r8 | % Coda 12
  b,8-. <fs b ds'>8-. fs,8-. <fs b ds'>8-. | % Coda 13
  d8-. <fs a bs>8-. d,8-. <fs a bs>8-. | % Coda 14
  cs8-. <fs as cs'>8-. cs,8-. <es gs b>8-. | % Coda 15
  fs,8-. <as cs' fs'>8-. fs,8-. r8 | % Coda 16
  <fs,, fs,>8 <as cs' fs'>8 <cs, cs>8 <as cs' fs'>8 | % Coda 17
  <fs,, fs,>8 <as cs' fs'>8 <cs, cs>8 r8 | % Coda 18
  <cs, cs>8 <es gs b>8 <gs,, gs,>8 <es gs b>8 | % Coda 19
  <cs, cs>8 <es gs b>8 <gs,, gs,>8 r8 | % Coda 20
  <b,, b,>8 <fs b ds'>8 <fs,, fs,>8 <fs b ds'>8 | % Coda 21
  <gs,, gs,>8 <gs b ds'>8 <ds, ds>8 <gs b ds'>8 | % Coda 22
  <cs, cs>8 <fs as cs'>8 <cs, cs>8 <es gs b>8 | % Coda 23
  <fs,, fs,>8 <as cs' fs'>8 <fs,, fs,>8 r8 | % Coda 24
  <fs,, fs,>8 <as cs' fs'>8 <cs, cs>8 <as cs' fs'>8 | % Coda 25
  <fs,, fs,>8 <as cs' fs'>8 <cs, cs>8 r8 | % Coda 26
  <cs, cs>8 <es gs b>8 <gs,, gs,>8 <es gs b>8 | % Coda 27
  <cs, cs>8 <es gs b>8 <gs,, gs,>8 r8 | % Coda 28
  <b,, b,>8 <fs b ds'>8 <fs,, fs,>8 <fs b ds'>8 | % Coda 29
  <d, d>8 <fs a bs>8 \ottava #-1 <d,, d,>8 \ottava #0 <fs a bs>8 | % Coda 30
  <cs, cs>8 <fs as cs'>8 <cs, cs>8 <fs as cs'>8 | % Coda 31
  <cs, cs>8 <es gs b>8 <cs, cs>8 <es gs b>8 | % Coda 32
  <bs,, bs,>32 r32 <d, d>32 r32 <e, e>32 r32 <fs, fs>32 r32 <gs, gs>32 r32 <as, as>32 r32 <bs, bs>32 r32 <d d'>32 r32 | % Coda 33
  <e e'>32 r32 <fs fs'>32 r32 <gs gs'>32 r32 <as as'>32 r32 \clef treble <bs bs'>32 r32 <d' d''>32 r32 <e' e''>32 r32 r16 | % Coda 34
  \clef bass <fs,, fs,>4 \clef treble r32 <ds'' ds'''>32 r32 <b' b''>32 r32 <gs' gs''>32 r32 <es' es''>32 | % Coda 35
  r32 <cs' cs''>32 r32 <as as'>32 r32 <fs fs'>32 r32 <ds ds'>32 \clef bass r32 <b, b>32 r32 <gs, gs>32 r32 r32 r16 | % Coda 36
  <ds, ds>32 r32 <ds, ds>32 r32 <ds, ds>32 r32 <ds, ds>32 r32 <d, d>32 r32 <d, d>32 r32 <d, d>32 r32 <d, d>32 r32 | % Coda 37
  <cs, cs>32 r32 <cs, cs>32 r32 <cs, cs>32 r32 <cs, cs>32 r32 <cs, cs>32 r32 <cs, cs>32 r32 <cs, cs>32 r32 <cs, cs>32 r32 | % Coda 38
  <cs, cs>32 r32 <cs, cs>32 r32 <cs, cs>32 r32 <cs, cs>32 r32 <cs, cs>32 r32 <cs, cs>32 r32 <cs, cs>32 r32 <cs, cs>32 r32 | % Coda 39
  <cs, cs>8 <cs, cs>8 \ottava #-1 <cs,, cs,>8 \ottava #0 r8 | % Coda 40
  <fs,, fs,>8 cs16 fs16 as16 cs'16 fs'16 as'16 | % Coda 41
  <fs as cs'>8 r8 <fs, cs fs>8 r8 | % Coda 42
  <cs, cs>4 <fs,, fs,>4 | % Coda 43
  <fs,, fs,>2\fermata \bar "|." | % Coda 44
}

\score {
  \new PianoStaff <<
    \new Staff = "up" \upper
    \new Staff = "down" \lower
  >>
  \layout { }
}

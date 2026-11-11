\version "2.24.4"
\language "english"
#(set-global-staff-size 17)
\header {
  title = "The Last Lamp"
  subtitle = "Nocturne in F minor"
  subsubtitle = "Concert version for solo piano"
  composer = "Composed with Codex, 2026"
  poet = "In the manner of Chopin"
  tagline = ##f
}
\paper {
  #(set-paper-size "a4")
  page-count = #6
  top-margin = 13\mm bottom-margin = 13\mm
  left-margin = 14\mm right-margin = 14\mm
  system-system-spacing.basic-distance = #20
  ragged-last-bottom = ##f
}

upper = {
  \clef treble \time 12/8 \tempo "Lento espressivo" 4. = 49
  \override TupletBracket.bracket-visibility = ##f
  \key f \minor  R1. | % 1
    r2. r4. c''4\p^\markup\italic "cantabile" df''8 | \break % 2
    << { \voiceOne af''4.\p( af''4 g''8 c'''4. \tuplet 7/6 { c'''16 df''' c''' bf'' af'' g'' af'' } } \new Voice { \voiceTwo c''4. ef''4. f''4. e''8 f''8 c''8 } >> \oneVoice | % 3
    << { \voiceOne g''4. f''4. e''4. \tuplet 7/6 { df''16 e'' f'' e'' df'' c'' bf' } } \new Voice { \voiceTwo df''4. bf'4. bf'4. s4. } >> \oneVoice | % 4
    << { \voiceOne c''4.\< c''8 af'4 f''4. \tuplet 9/12 { a''32 bf'' a'' g'' f'' e'' f'' g'' a'' } } \new Voice { \voiceTwo s2. c''4. ef''4. } >> \oneVoice | % 5
    << { \voiceOne bf''4.\mp bf''4 af''8 f''4. ef''4\> df''8) } \new Voice { \voiceTwo df''2. bf'2. } >> \oneVoice | \break % 6
    << { \voiceOne c''4.\p( ef''4 c''8 af''4. \tuplet 4/3 { g''8 af'' g'' f'' } } \new Voice { \voiceTwo s2. f''4. df''4. } >> \oneVoice | % 7
    << { \voiceOne e''4. g''4 g''8 bf''4. \tuplet 7/6 { a''16 g'' f'' e'' g'' f'' e'' } } \new Voice { \voiceTwo bf'4. c''4. e''4. s4. } >> \oneVoice | % 8
    af''4.^\markup\italic "poco rit." f''4. df''4 c''8 b'8 c''4) | % 9
    g'4. \tuplet 9/12 { bf'32 c'' e'' g'' bf'' a'' g'' e'' g'' } g''4.\pp\breathe r4. | \break % 10
    <af' af''>4.\p^\markup\italic "a tempo"( af''4 g''8 <c'' c'''>4. \tuplet 8/6 { ef'''16 df''' c''' bf'' af'' g'' af'' c''' } | % 11
    <ef'' c'''>4.\mp <ef'' c'''>4 <c'' af''>8 <bf' g''>4. \acciaccatura af''8 <af' f''>4 <g' ef''>8 | % 12
    df''4. \tuplet 8/6 { df''16 ef'' df'' c'' bf' c'' df'' f'' } bf''4. \tuplet 8/6 { af''16 bf'' af'' gf'' f'' ef'' df'' f'' } | % 13
    <c'' a''>4. <ef'' c'''>8 <d'' bf''>8 <c'' a''>8 <bf' g''>4. <g' ef''>4 <af' f''>8) | \break % 14
    e''4.\<( g''16 af'' g'' f'' e'' g'' c'''4. af''16 bf'' af'' g'' f'' g'' | % 15
    gf''4.\mp \tuplet 8/6 { gf''16 af'' gf'' f'' ef'' df'' c'' df'' } e''4. \tuplet 8/6 { df''16 e'' df'' c'' bf' af' g' bf' } | % 16
    c''4.\> df''32 c'' bf' g' e' g' bf' c'' df'' e'' f'' e'' e''4. \tuplet 8/6 { e''16 f'' e'' d'' c'' bf' g' e'' }) | % 17
    f''2.\p\breathe r4. ef''8 f''8 g''8 | \bar "||" \break % 18
  \key af \major \tempo "Poco piu mosso, dolce" 4. = 53 << { \voiceOne af''4.\pp^\markup\italic "due voci"( af''4 bf''8 c'''4. ef'''4 c'''8 } \new Voice { \voiceTwo c''4 ef''8 f''4~ f''8 ef''4 g''8 bf''4 g''8 } >> \oneVoice | % 19
    << { \voiceOne bf''4. g''4 ef''8 c'''4. bf''4 af''8 } \new Voice { \voiceTwo ef''4 df''8 bf'4 g'8 ef''4 c''8 ef''4 c''8 } >> \oneVoice | % 20
    << { \voiceOne c''4.\< ef''4. af''4. g''4 f''8 } \new Voice { \voiceTwo af'4. bf'4 c''8 f''4. ef''4 df''8 } >> \oneVoice | % 21
    << { \voiceOne ef''4. g''4. bf''4.~\mp bf''8 bf''8 g''8) } \new Voice { \voiceTwo bf'4 df''8 ef''4 df''8 f''4. ef''4 df''8 } >> \oneVoice | \break % 22
    << { \voiceOne f''4.\p( f''8 g''8 af''8 df'''4. c'''4 bf''8 } \new Voice { \voiceTwo df''4. ef''4 f''8 f''4 ef''8 c''4. } >> \oneVoice | % 23
    << { \voiceOne a''4. a''4 f''8 bf''4.\mp df'''4 bf''8 } \new Voice { \voiceTwo c''4 ef''8 ef''4. df''4. f''4 df''8 } >> \oneVoice | % 24
    << { \voiceOne af''4.\> c'''4 af''8 g''4. ef''4 bf'8) } \new Voice { \voiceTwo ef''4. df''4 c''8 bf'4. g'4. } >> \oneVoice | % 25
    af'2.\pp\breathe r4. c''8 df''8 ef''8 | \bar "||" \break % 26
   \tempo "Poco a poco agitato" 4. = 58 <df'' f''>4.\p( <ef'' gf''>16 <f'' af''>16 <ef'' gf''>16 <df'' f''>16 <c'' ef''>16 <bf' df''>16 <ef'' af''>4. <gf'' bf''>8 <f'' af''>8 <ef'' gf''>8 | % 27
    <c'' ef''>4. <bf' df''>4 <af' c''>8 <f' bf'>4. <bf' df''>8 <c'' ef''>8 <df'' f''>8 | % 28
    << { \voiceOne f''4.\mp^\markup\italic "cresc. e stringendo" af''4. df'''4. \tuplet 8/6 { c'''16 df''' c''' bf'' af'' gf'' f'' af'' } } \new Voice { \voiceTwo s2. bf''4. s4. } >> \oneVoice | % 29
    <c'' a''>4. <ef'' c'''>4 <c'' a''>8 <bf' g''>4. <g' e''>4 <g' e''>8) | \break % 30
    <df'' f''>4.\mf( <f'' af''>4 <df'' f''>8 <f'' df'''>4. <c'' af''>4 <c'' af''>8 | % 31
    <e' c''>4 <f' df''>8 <g' e''>4. <e'' g''>4 <f'' af''>8 <g'' bf''>4. | % 32
    <gf'' bf''>4.\f <bf'' df'''>4 <af'' c'''>8 <g'' bf''>4. <f'' af''>4 <e'' gf''>8 | % 33
    <c'' f''>4. <ef'' af''>4 <c'' f''>8 <e'' c'''>4. <e'' c'''>4 <e'' df'''>16 <e'' c'''>16) | \break % 34
    <af' af''>4.\f\<( <f'' af''>16 <g'' bf''>16 <af'' c'''>8 <f'' af''>8 <b' d'' b''>4. <f'' d'''>8. <e'' c'''>16 <d'' b''>8 | % 35
    <df'' gf'' df'''>4~ <df'' gf'' df'''>16 <df'' gf'' df'''>16 <c'' ef'' c'''>4 <bf' df'' bf''>8 <c'' ef'' g'' c'''>4. <g'' ef'''>4 <g'' e'''>8 | % 36
   \tempo "Allargando" 4. = 43 <b'' f'''>4.\ff-> <af'' ef'''>8. <f'' df'''>16 <af'' b''>8 <f'' af'' c'''>4. <af'' bf''>4 <f'' af''>8 | % 37
    <e'' g''>4.\f\> <df'' f''>4 <c'' e''>8 <bf' df''>4. <g' c''>4.\p) | \break % 38
   \tempo "Quasi cadenza" c'''4.\trill\mp\fermata \tuplet 52/36 { c'''32^\markup\italic "leggiero, dim." df''' c''' bf'' g'' e'' df'' e'' g'' bf'' df''' e''' g''' f''' e''' df''' c''' bf'' af'' g'' f'' e'' df'' c'' bf' g' e' g' bf' df'' e'' g'' bf'' df''' c''' bf'' af'' g'' f'' e'' df'' c'' bf' g' e' g' bf' c'' df'' e'' g'' c''' } | \noPageBreak % 39
    df''4.\pp c''4.\breathe r2. | \bar "||" \pageBreak % 40
  \key f \minor \tempo "Tempo I" 4. = 49 << { \voiceOne af''4.\pp^\markup\italic "sotto voce"( af''4 g''8 c'''4. \tuplet 11/12 { c'''32 df''' c''' bf'' af'' g'' af'' c''' bf'' g'' af'' } } \new Voice { \voiceTwo c''8 ef''16 f''16 ef''16 df''16 c''8 df''16 ef''16 f''8 f''8 e''16 f''16 af''8 s4. } >> \oneVoice | % 41
    << { \voiceOne g''4. f''4. e''4. \tuplet 13/12 { df''32 e'' g'' bf'' df''' c''' bf'' g'' e'' df'' c'' bf' c'' } } \new Voice { \voiceTwo df''4. bf'4. s2. } >> \oneVoice | % 42
    << { \voiceOne c''4.\p c''8 af'4 f''4. \tuplet 13/12 { a''32 bf'' a'' g'' f'' e'' f'' g'' a'' c''' bf'' a'' f'' } } \new Voice { \voiceTwo s2. c''4. s4. } >> \oneVoice | % 43
    << { \voiceOne bf''4.\mp bf''4 af''8 f''4. \tuplet 13/12 { ef''32 f'' ef'' df'' c'' df'' ef'' f'' ef'' df'' c'' bf' df'' }) } \new Voice { \voiceTwo df''4. f''4. bf'4. s4. } >> \oneVoice | \break % 44
    << { \voiceOne c''4.\p( ef''4 c''8 af''4. \tuplet 13/12 { g''32 af'' bf'' af'' g'' f'' e'' f'' g'' af'' g'' f'' df'' } } \new Voice { \voiceTwo af'2. f''4. s4. } >> \oneVoice | % 45
    << { \voiceOne e''4. \tuplet 11/12 { g''32 af'' g'' f'' e'' g'' bf'' af'' g'' e'' g'' } g''4. e''4\trill df''8 } \new Voice { \voiceTwo bf'4. s4. s2. } >> \oneVoice | % 46
    c''4.\> af'4. bf'4 af'8 g'8 f'4) | % 47
    e'4. g'4 bf'8 c''4.\pp f''4.\breathe | \pageBreak % 48
    af''2.\p^\markup\italic "come un ricordo"( g''4. f''4. | % 49
    gf''4. gf''4 f''8 e''4. df''4 bf'8 | % 50
    e''4.\pp^\markup\italic "rit." g''4 f''8 e''4. df''4.) | % 51
    c''2.\pp\breathe r2. | \bar "||" \break % 52
  \key f \major \tempo "Tranquillo" 4. = 47 << { \voiceOne a''4.\pp^\markup\italic "dolcissimo"( a''4 g''8 c'''4. c'''4 a''8 } \new Voice { \voiceTwo c''4. d''4 e''8 f''4. e''8 d''8 c''8 } >> \oneVoice | % 53
    << { \voiceOne g''4. f''4. e''4. c''4. } \new Voice { \voiceTwo d''4. bf'4. g'4. bf'4. } >> \oneVoice | % 54
    << { \voiceOne d''4. f''4 d''8 bf''4. a''4 f''8 } \new Voice { \voiceTwo a'2. d''4. f''4 d''8 } >> \oneVoice | % 55
    << { \voiceOne a'4. c''4. f''4. e''4 d''8) } \new Voice { \voiceTwo f'4. a'4. df''4. c''4 bf'8 } >> \oneVoice | \break % 56
    << { \voiceOne df''4.^\markup\italic "perdendosi"( c''4. bf'4. af'4. } \new Voice { \voiceTwo af'4. f'4. df'4. f'4. } >> \oneVoice | % 57
    a'4. g'4 f'8 e'4. c''4. | % 58
    << { \voiceOne f''4.\ppp \tuplet 11/12 { e''16 f'' g'' a'' c''' bf'' a'' g'' f'' e'' f'' } c''4.) } \new Voice { \voiceTwo c''4. s4. s2. } >> \oneVoice | % 59
    <a' c'' f''>1.\ppp\arpeggio\fermata | % 60
  \bar "|."
}

lower = {
  \clef bass \time 12/8
  \key f \minor f,8\pp_\markup\italic "legato, con pedale; sempre delicato"( c8 f8 af8 c'8 af8 f,8 c8 af8 c'8 af8 f8) | % 1
   f,8( c8 f8 af8 c'8 af8 c,8 g,8 e8 bf8 e8 df8) | \break % 2
   f,8( c8 af8 c'8 af8 f8 f,8 f8 af8 c'8 af8 c8) | % 3
   df8( f8 df'8 f'8 df'8 bf8 c,8 df8 e8 bf8 e8 g,8) | % 4
   f,8( c8 af8 c'8 af8 f8 f,8 ef8 a8 c'8 a8 c8) | % 5
   df8( bf8 df'8 f'8 df'8 f8 df8 ef8 g8 bf8 df'8 g8) | \break % 6
   c8( af8 c'8 ef'8 c'8 ef8 df,8 af,8 df8 f8 af8 f8) | % 7
   c,8( c8 e8 bf8 e8 g,8 c,8 g,8 c8 e8 bf8 e8) | % 8
   df,8( af,8 df8 f8 af8 f8 c,8 g,8 df8 e8 bf8 e8) | % 9
   c,8 g,8 c8 e8 bf8 e8 c,8 e8 bf8 r4. | \break % 10
   f,16( c16 f16 af16 c'16 f'16 c'16 af16 f16 c16 af,16 c16 ef,16 af,16 c16 ef16 af16 c'16 ef'16 c'16 af16 ef16 c16 af,16) | % 11
   c,16( af,16 c16 ef16 af16 c'16 ef'16 c'16 af16 ef16 c16 af,16 bf,,16 g,16 bf,16 df16 ef16 g16 bf16 g16 ef16 df16 bf,16 g,16) | % 12
   df,16( bf,16 df16 f16 bf16 df'16 f'16 df'16 bf16 f16 df16 bf,16 bf,,16 f,16 af,16 df16 f16 af16 f16 df16 bf,16 af,16 f,16 df,16) | % 13
   c,16( a,16 c16 ef16 f16 a16 c'16 a16 f16 ef16 c16 a,16 g,16 bf,16 df16 ef16 g16 bf16 df'16 bf16 g16 ef16 df16 bf,16) | \break % 14
   c,16( g,16 c16 e16 g16 bf16 c'16 bf16 g16 e16 c16 g,16 c,16 af,16 c16 f16 af16 c'16 f'16 c'16 af16 f16 c16 af,16) | % 15
   bf,,16( gf,16 bf,16 df16 gf16 bf16 df'16 bf16 gf16 df16 bf,16 gf,16 bf,,16 g,16 bf,16 df16 e16 g16 bf16 g16 e16 df16 bf,16 g,16) | % 16
   c,16( g,16 c16 e16 g16 bf16 c'16 bf16 g16 e16 c16 g,16 c,16 g,16 c16 e16 g16 bf16 c'16 bf16 g16 e16 c16 g,16) | % 17
   f,4. <c af>4. r4. ef8 g8 bf8 | \bar "||" \break % 18
  \key af \major c8( af8 c'8 ef'8 c'8 ef8 g,8 bf,8 df8 ef8 bf8 df8) | % 19
   g,8( df8 ef8 bf8 ef8 bf,8 af,8 ef8 af8 c'8 ef'8 c'8) | % 20
   c8( ef8 af8 c'8 ef'8 af8 df,8 af,8 df8 f8 af8 f8) | % 21
   bf,8( ef8 g8 bf8 df'8 g8 ef,8 bf,8 ef8 g8 df'8 g8) | \break % 22
   df,8( af,8 df8 f8 af8 f8 a,8 c8 ef8 f8 c'8 a8) | % 23
   a,8( c8 ef8 f8 c'8 a8 df8 f8 bf8 df'8 bf8 af8) | % 24
   c8( ef8 af8 c'8 ef'8 af8 ef,8 bf,8 g8 df'8 g8 ef8) | % 25
   af,8 ef8 af8 c'8 ef'8 c'8 r4. c8 ef8 gf8 | \bar "||" \break % 26
   df,16( af,16 df16 f16 af16 df'16 f'16 df'16 af16 f16 df16 af,16 c,16 af,16 c16 ef16 gf16 af16 c'16 af16 gf16 ef16 c16 af,16) | % 27
   c,16( af,16 c16 ef16 gf16 af16 c'16 af16 gf16 ef16 c16 af,16 bf,,16 f,16 bf,16 df16 f16 bf16 f16 df16 bf,16 f,16 df,16 f,16) | % 28
   df,16( af,16 df16 f16 af16 df'16 f'16 df'16 af16 f16 df16 af,16 gf,16 df16 gf16 bf16 df'16 gf'16 df'16 bf16 gf16 df16 bf,16 df16) | % 29
   a,16( c16 ef16 f16 a16 c'16 ef'16 c'16 a16 f16 ef16 c16 e,16 g,16 bf,16 c16 e16 g16 c'16 g16 e16 c16 bf,16 g,16) | \break % 30
   f,16( bf,16 df16 f16 af16 df'16 f'16 df'16 af16 f16 df16 bf,16 f,16 af,16 df16 f16 af16 df'16 f'16 df'16 af16 f16 df16 af,16) | % 31
   e,16( g,16 bf,16 c16 e16 g16 c'16 g16 e16 c16 bf,16 g,16 c,16 g,16 bf,16 df16 e16 g16 bf16 g16 e16 df16 bf,16 g,16) | % 32
   bf,,16( gf,16 bf,16 df16 gf16 bf16 df'16 bf16 gf16 df16 bf,16 gf,16 bf,,16 g,16 bf,16 df16 e16 g16 bf16 g16 e16 df16 bf,16 g,16) | % 33
   c,16( af,16 c16 f16 af16 c'16 f'16 c'16 af16 f16 c16 af,16 c,16 g,16 bf,16 df16 e16 g16 bf16 g16 e16 df16 bf,16 g,16) | \break % 34
   df,16( af,16 df16 f16 af16 df'16 f'16 df'16 af16 f16 df16 af,16 d,16 af,16 b,16 d16 f16 af16 b16 af16 f16 d16 b,16 af,16) | % 35
   ef,16( bf,16 df16 gf16 bf16 df'16 gf'16 df'16 bf16 gf16 df16 bf,16 g,16 bf,16 df16 ef16 g16 bf16 df'16 bf16 g16 ef16 df16 bf,16) | % 36
   df,16( af,16 b,16 df16 f16 af16 b16 af16 f16 df16 b,16 af,16 c,16 af,16 c16 f16 af16 c'16 f'16 c'16 af16 f16 c16 af,16) | % 37
   c,16( g,16 bf,16 df16 e16 g16 bf16 g16 e16 df16 bf,16 g,16 <c e bf>2.) | \break % 38
   <c g bf>1. | \noPageBreak % 39
   \tuplet 19/24 { c,32 g, c e g bf \clef treble df' e' g' bf' g' e' df' \clef bass bf g e c g, c, } r2. | \bar "||" \pageBreak % 40
  \key f \minor f,16( c16 f16 af16 c'16 f'16 c'16 af16 f16 c16 af,16 c16 f,16 c16 f16 af16 c'16 f'16 c'16 af16 f16 c16 af,16 c16) | % 41
   df,16( bf,16 df16 f16 bf16 df'16 f'16 df'16 bf16 f16 df16 bf,16 c,16 g,16 bf,16 df16 e16 g16 bf16 g16 e16 df16 bf,16 g,16) | % 42
   f,16( c16 f16 af16 c'16 f'16 c'16 af16 f16 c16 af,16 c16 f,16 c16 ef16 a16 c'16 ef'16 c'16 a16 f16 ef16 c16 a,16) | % 43
   df,16( bf,16 df16 f16 bf16 df'16 f'16 df'16 bf16 f16 df16 bf,16 df,16 bf,16 df16 ef16 g16 bf16 df'16 bf16 g16 ef16 df16 bf,16) | \break % 44
   c,16( af,16 c16 ef16 af16 c'16 ef'16 c'16 af16 ef16 c16 af,16 df,16 af,16 df16 f16 af16 df'16 f'16 df'16 af16 f16 df16 af,16) | % 45
   c,16( g,16 bf,16 df16 e16 g16 bf16 g16 e16 df16 bf,16 g,16 c,16 g,16 bf,16 df16 e16 g16 bf16 g16 e16 df16 bf,16 g,16) | % 46
   af,8( c8 f8 af8 c'8 f8 f,8 bf,8 df8 f8 bf8 df8) | % 47
   c,8( g,8 c8 e8 g8 bf8 f,4. <c af>4.) | \pageBreak % 48
   f,8( af,8 df8 f8 af8 df8 c8 f8 c'8 af8 c'8 af8) | % 49
   bf,8( df8 gf8 bf8 df'8 gf8 bf,8 df8 g8 bf8 g8 e8) | % 50
   c,8( g,8 e8 bf8 e8 df8 c,8 df8 e8 bf8 e8 g,8) | % 51
   <c e bf>2. r2. | \bar "||" \break % 52
  \key f \major f,8( c8 a8 c'8 a8 f8 f,8 f8 a8 c'8 a8 c8) | % 53
   bf,8( f8 g8 bf8 g8 d8 c,8 g,8 c8 e8 bf8 e8) | % 54
   d,8( d8 f8 a8 f8 a,8 d8 f8 bf8 d'8 f'8 bf8) | % 55
   a,8( f8 a8 c'8 a8 c8 df8 f8 bf8 df'8 f'8 bf8) | \break % 56
   df8( f8 af8 bf8 df'8 af8 df8 f8 af8 bf8 df'8 af8) | % 57
   c8( f8 a8 c'8 a8 f8 c,8 g,8 c8 e8 bf8 e8) | % 58
   f,4. c4. a4. c'4. | % 59
   <f, c f>1.\arpeggio\fermata | % 60
  \bar "|."
}

\score {
  \new PianoStaff \with { connectArpeggios = ##t } <<
    \new Staff = "upper" \upper
    \new Staff = "lower" \lower
  >>
  \layout {
    \context { \Score \override SpacingSpanner.common-shortest-duration = #(ly:make-moment 1/16) }
  }
  \midi { }
}

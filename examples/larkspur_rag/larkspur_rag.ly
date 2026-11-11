\version "2.24.0"
\language "english"
\header {
  title = "Larkspur Rag"
  subtitle = "a classic rag for piano"
  composer = "Claude, 2026"
  poet = "in the manner of Scott Joplin"
  tagline = ##f
}
\paper {
  #(set-paper-size "a4")
  top-margin = 12\mm  bottom-margin = 12\mm  left-margin = 13\mm  right-margin = 13\mm
  system-system-spacing.basic-distance = #16
  ragged-last-bottom = ##f
}
upper = {
  \clef treble \key ef \major \time 2/4 \tempo "Not fast" 4 = 92
  
    <ef' ef''>16\f <g' g''>16 <bf' bf''>16 <c'' c'''>16~ <c'' c'''>16 <bf' bf''>16 <g' g''>16 <ef' ef''>16 | % Intro 1
    <f' f''>16 <af' af''>16 <bf' bf''>16 <d'' d'''>16~ <d'' d'''>16 <bf' bf''>16 <af' af''>16 <f' f''>16 | % Intro 2
    <g' g''>16 <bf' bf''>16 <ef'' ef'''>16 <f'' f'''>16~ <f'' f'''>16 <ef'' ef'''>16 <c'' c'''>16 <a' a''>16 | % Intro 3
    <af' bf' d''>8 r8 <af' bf' d'' f''>8 r8 | % Intro 4
  \repeat volta 2 {
    <g' g''>8\mf ef''16 <g' g''>16~ <g' g''>16 ef''16 <g' bf'>8 | % A 1
    c''16 d''16 ef''16 <c'' c'''>16~ <c'' c'''>16 bf''16 g''16 ef''16 | % A 2
    <f' f''>8 d''16 <f' f''>16~ <f' f''>16 d''16 af'8 | % A 3
    bf'16 c''16 d''16 <bf' bf''>16~ <bf' bf''>16 af''16 f''16 d''16 | % A 4
    f''16 e''16 ef''16 d''16 c''16 bf'16 af'16 g'16 | % A 5
    <f' af'>8 bf'16 <af' d''>16~ <af' d''>16 f''16 ef''16 d''16 | % A 6
    <g' ef''>8 bf'16 <g' ef''>16~ <g' ef''>16 bf'16 g'8 | % A 7
    <g' bf' ef''>4 r16 e''16 f''16 gf''16 | % A 8
    <g' g''>8 ef''16 <g' g''>16~ <g' g''>16 ef''16 <g' bf'>8 | % A 9
    df''16 ef''16 f''16 <df'' g''>16~ <df'' g''>16 f''16 ef''16 df''16 | % A 10
    <af' af''>8 ef''16 <af' af''>16~ <af' af''>16 ef''16 c''8 | % A 11
    <af' af''>8 <cf'' gf''>8 <af' ff''>8 <af' ef''>8 | % A 12
    bf'16\< ef''16 g''16 <bf' bf''>16~ <bf' bf''>16 af''16 g''16 ef''16 | % A 13
    e''16 g''8 bf''16 <e'' c'''>16 bf''8 g''16 | % A 14
    f''16\! g''16 a''16 c'''16 bf''16 af''16 f''16 d''16 | % A 15
    <g' bf' ef''>8 <af' bf' d''>8 <g' bf' ef''>4 | % A 16
  }
  \repeat volta 2 {
    <af' af''>16\f f''8 d''16 <af' af''>16 f''8 d''16 | % B 1
    c''16 d''16 f''16 <bf' bf''>16~ <bf' bf''>16 af''16 g''16 f''16 | % B 2
    <g' g''>16 ef''8 bf'16 <g' g''>16 ef''8 bf'16 | % B 3
    g''16 f''16 ef''16 d''16 <g' bf' ef''>4 | % B 4
    <g' g''>16 d''8 b'16 <g' g''>16 d''8 b'16 | % B 5
    a'16 b'16 d''16 <g' g''>16~ <g' g''>16 f''16 ef''16 d''16 | % B 6
    <g' g''>16 ef''8 c''16 <g' g''>16 ef''8 c''16 | % B 7
    <g' c''>4 r16 g'16 a'16 b'16 | % B 8
    <af' c''>8.^\markup\italic"broadly" bf'16 <af' c''>8 <c'' ef''>8 | % B 9
    <c'' ef''>8. d''16 <c'' ef''>8 <ef'' gf''>8 | % B 10
    <g' g''>8 ef''16 <g' g''>16~ <g' g''>16 ef''16 bf'8 | % B 11
    <e' e''>8 c''16 e''16~ e''16 c''16 bf'8 | % B 12
    <ef' ef''>8 c''16 ef''16~ ef''16 c''16 a'8 | % B 13
    bf'16 c''16 d''16 f''16 af''16 g''16 f''16 d''16 | % B 14
    ef''16 f''16 g''16 <ef'' ef'''>16~ <ef'' ef'''>16 d'''16 c'''16 bf''16 | % B 15
    <g' bf' ef''>8 <af' bf' d''>8 <g' bf' ef''>4 | % B 16
  }
  
    <g' g''>8\mf ef''16 <g' g''>16~ <g' g''>16 ef''16 <g' bf'>8 | % A2 1
    c''16 d''16 ef''16 <c'' c'''>16~ <c'' c'''>16 bf''16 g''16 ef''16 | % A2 2
    <f' f''>8 d''16 <f' f''>16~ <f' f''>16 d''16 af'8 | % A2 3
    bf'16 c''16 d''16 <bf' bf''>16~ <bf' bf''>16 af''16 f''16 d''16 | % A2 4
    f''16 e''16 ef''16 d''16 c''16 bf'16 af'16 g'16 | % A2 5
    <f' af'>8 bf'16 <af' d''>16~ <af' d''>16 f''16 ef''16 d''16 | % A2 6
    <g' ef''>8 bf'16 <g' ef''>16~ <g' ef''>16 bf'16 g'8 | % A2 7
    <g' bf' ef''>4 r16 e''16 f''16 gf''16 | % A2 8
    <g' g''>8 ef''16 <g' g''>16~ <g' g''>16 ef''16 <g' bf'>8 | % A2 9
    df''16 ef''16 f''16 <df'' g''>16~ <df'' g''>16 f''16 ef''16 df''16 | % A2 10
    <af' af''>8 ef''16 <af' af''>16~ <af' af''>16 ef''16 c''8 | % A2 11
    <af' af''>8 <cf'' gf''>8 <af' ff''>8 <af' ef''>8 | % A2 12
    bf'16 ef''16 g''16 <bf' bf''>16~ <bf' bf''>16 af''16 g''16 ef''16 | % A2 13
    e''16 g''8 bf''16 <e'' c'''>16 bf''8 g''16 | % A2 14
    f''16 g''16 a''16 c'''16 bf''16 af''16 f''16 d''16 | % A2 15
    <g' bf' ef''>8 <af' bf' d''>8 <g' bf' ef''>4 | % A2 16
  \bar "||"
  \key af \major \mark \markup\bold"Trio" \repeat volta 2 {
    c''8\p^\markup\italic"dolce, cantabile" <af' ef''>8~ <af' ef''>16 ef''16 f''16 g''16 | % C 1
    <c'' af''>8. g''16 f''8 ef''8 | % C 2
    bf'8 <g' df''>8~ <g' df''>16 df''16 ef''16 f''16 | % C 3
    <bf' g''>8. f''16 ef''8 df''8 | % C 4
    g'16 bf'16 df''16 g''16~ g''16 f''16 ef''16 df''16 | % C 5
    bf'16 df''16 ef''16 bf''16~ bf''16 af''16 g''16 ef''16 | % C 6
    <af' c''>8. bf'16 c''8 ef''8 | % C 7
    <c'' ef'' af''>4 r16 af'16 bf'16 b'16 | % C 8
    c''8 <af' ef''>8~ <af' ef''>16 ef''16 f''16 g''16 | % C 9
    <c'' af''>8. gf''16 f''8 ef''8 | % C 10
    f''8\< <df'' af''>8~ <df'' af''>16 af''16 bf''16 c'''16 | % C 11
    <ff'' df'''>8. cf'''16 bff''8 af''8 | % C 12
    ef''16\mf af''16 c'''16 <ef'' ef'''>16~ <ef'' ef'''>16 df'''16 c'''16 af''16 | % C 13
    f''16 a''16 c'''16 ef'''16~ ef'''16 d'''16 c'''16 a''16 | % C 14
    d''16\> f''16 af''16 bf''16 df''16 ef''16 g''16 bf''16 | % C 15
    <c'' ef'' af''>8\! <df'' ef'' g''>8 <c'' ef'' af''>4 | % C 16
  }
  \key ef \major \repeat volta 2 {
    <ef' ef''>8\f^\markup\italic"2nd time ff" c''16 <af' ef''>16~ <af' ef''>16 c''16 af'8 | % D 1
    a'16 c''8 d''16 ef''8 c''8 | % D 2
    <g' g''>8 ef''16 <g' g''>16~ <g' g''>16 ef''16 bf'8 | % D 3
    g'16 bf'8 c''16 e''8 c''8 | % D 4
    <af' f''>8 c''16 <af' f''>16~ <af' f''>16 c''16 af'8 | % D 5
    f''16 ef''16 d''16 c''16 bf'16 a'16 c''16 ef''16 | % D 6
    <f' d''>8 bf'16 <f' d''>16~ <f' d''>16 bf'16 af'8 | % D 7
    <af' bf' d''>4 r16 bf''16 c'''16 d'''16 | % D 8
    <ef'' ef'''>8^\markup\italic"brillante" c'''16 <ef'' ef'''>16~ <ef'' ef'''>16 c'''16 af''8 | % D 9
    a''16 c'''8 d'''16 <ef'' ef'''>8 c'''8 | % D 10
    <g'' g'''>8 ef'''16 <g'' g'''>16~ <g'' g'''>16 ef'''16 bf''8 | % D 11
    g''16 bf''8 c'''16 <e'' e'''>8 c'''8 | % D 12
    a''16 c'''8 ef'''16 <f'' f'''>16 ef'''8 c'''16 | % D 13
    d'''16 c'''16 bf''16 af''16 f''16 g''16 af''16 bf''16 | % D 14
    g''16 af''16 bf''16 <g'' g'''>16~ <g'' g'''>16 f'''16 ef'''16 bf''16 | % D 15
    <g'' bf'' ef'''>8 <af'' bf'' d'''>8 <g'' bf'' ef'''>4\fermata | % D 16
  }
  \bar "|."
}
lower = {
  \clef bass \key ef \major \time 2/4
  
    ef16 g16 bf16 c'16~ c'16 bf16 g16 ef16 | % Intro 1
    f16 af16 bf16 d'16~ d'16 bf16 af16 f16 | % Intro 2
    g16 bf16 ef'16 f'16~ f'16 ef'16 c'16 a16 | % Intro 3
    <bf,, bf,>8 r8 <bf,, bf,>8 r8 | % Intro 4
  \repeat volta 2 {
    <ef, ef>8_\markup\italic"a touch of pedal with each bass octave" <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % A 1
    <ef, ef>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % A 2
    <bf, bf>8 <af bf d'>8 <f, f>8 <af bf d'>8 | % A 3
    <bf, bf>8 <af bf d'>8 <f, f>8 <af bf d'>8 | % A 4
    <bf, bf>8 <d, d>8 <f, f>8 <af, af>8 | % A 5
    <f, f>8 <af bf d'>8 <bf, bf>8 <af bf d'>8 | % A 6
    <ef, ef>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % A 7
    <ef, ef>8 <g bf ef'>8 <bf,, bf,>8 <d, d>8 | % A 8
    <ef, ef>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % A 9
    <ef, ef>8 <g bf df'>8 <bf, bf>8 <g bf df'>8 | % A 10
    <af, af>8 <af c' ef'>8 <ef, ef>8 <af c' ef'>8 | % A 11
    <af, af>4 <af cf' ef'>4 | % A 12
    <bf,, bf,>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % A 13
    <c, c>8 <g bf e'>8 <g, g>8 <e, e>8 | % A 14
    <f, f>8 <a c' ef'>8 <bf,, bf,>8 <af bf d'>8 | % A 15
    <ef, ef>8 <bf,, bf,>8 <ef, ef>4 | % A 16
  }
  \repeat volta 2 {
    <bf, bf>8 <af bf d'>8 <f, f>8 <af bf d'>8 | % B 1
    <bf, bf>8 <af bf d'>8 <d, d>8 <af bf d'>8 | % B 2
    <ef, ef>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % B 3
    <ef, ef>8 <g bf ef'>8 <ef, ef>8 <f, f>8 | % B 4
    <g, g>8 <f g b>8 <d, d>8 <f g b>8 | % B 5
    <g, g>8 <f g b>8 <b, b>8 <f g b>8 | % B 6
    <c, c>8 <g c' ef'>8 <ef, ef>8 <g c' ef'>8 | % B 7
    <c, c>8 <g c' ef'>8 <c, c>8 <g, g>8 | % B 8
    <af, af>4 <af c' ef'>4 | % B 9
    <a, a>4 <gf c' ef'>4 | % B 10
    <bf,, bf,>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % B 11
    <c, c>8 <g bf e'>8 <g, g>8 <g bf e'>8 | % B 12
    <f, f>8 <a c' ef'>8 <c, c>8 <a c' ef'>8 | % B 13
    <bf,, bf,>8 <af bf d'>8 <f, f>8 <d, d>8 | % B 14
    <ef, ef>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % B 15
    <ef, ef>8 <bf,, bf,>8 <ef, ef>4 | % B 16
  }
  
    <ef, ef>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % A2 1
    <ef, ef>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % A2 2
    <bf, bf>8 <af bf d'>8 <f, f>8 <af bf d'>8 | % A2 3
    <bf, bf>8 <af bf d'>8 <f, f>8 <af bf d'>8 | % A2 4
    <bf, bf>8 <d, d>8 <f, f>8 <af, af>8 | % A2 5
    <f, f>8 <af bf d'>8 <bf, bf>8 <af bf d'>8 | % A2 6
    <ef, ef>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % A2 7
    <ef, ef>8 <g bf ef'>8 <bf,, bf,>8 <d, d>8 | % A2 8
    <ef, ef>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % A2 9
    <ef, ef>8 <g bf df'>8 <bf, bf>8 <g bf df'>8 | % A2 10
    <af, af>8 <af c' ef'>8 <ef, ef>8 <af c' ef'>8 | % A2 11
    <af, af>4 <af cf' ef'>4 | % A2 12
    <bf,, bf,>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % A2 13
    <c, c>8 <g bf e'>8 <g, g>8 <e, e>8 | % A2 14
    <f, f>8 <a c' ef'>8 <bf,, bf,>8 <af bf d'>8 | % A2 15
    <ef, ef>8 <bf,, bf,>8 <ef, ef>4 | % A2 16
  \bar "||"
  \key af \major \repeat volta 2 {
    <af, af>8_\markup\italic"legato pedal" <af c' ef'>8 <c, c>8 <af c' ef'>8 | % C 1
    <af, af>8 <af c' ef'>8 <ef, ef>4 | % C 2
    <ef, ef>8 <g bf df'>8 <bf, bf>8 <g bf df'>8 | % C 3
    <ef, ef>8 <g bf df'>8 <bf, bf>4 | % C 4
    <ef, ef>8 <g bf df'>8 <g, g>8 <g bf df'>8 | % C 5
    <bf, bf>8 <g bf df'>8 <ef, ef>8 <g bf df'>8 | % C 6
    <af, af>8 <af c' ef'>8 <ef, ef>8 <af c' ef'>8 | % C 7
    <af, af>8 <af c' ef'>8 <ef, ef>8 <g, g>8 | % C 8
    <af, af>8 <af c' ef'>8 <c, c>8 <af c' ef'>8 | % C 9
    <af, af>8 <gf c' ef'>8 <c, c>4 | % C 10
    <df, df>8 <af df' f'>8 <af, af>8 <af df' f'>8 | % C 11
    <df, df>4 <af df' ff'>4 | % C 12
    <ef, ef>8 <af c' ef'>8 <ef, ef>8 <af c' ef'>8 | % C 13
    <f, f>8 <a c' ef'>8 <c, c>8 <a c' ef'>8 | % C 14
    <bf,, bf,>8 <af bf d'>8 <ef, ef>8 <g bf df'>8 | % C 15
    <af, af>8 <ef, ef>8 <af,, af,>4 | % C 16
  }
  \key ef \major \repeat volta 2 {
    <af, af>8 <af c' ef'>8 <ef, ef>8 <af c' ef'>8 | % D 1
    <a, a>8 <gf c' ef'>8 <ef, ef>8 <gf c' ef'>8 | % D 2
    <bf,, bf,>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % D 3
    <c, c>8 <g bf e'>8 <g, g>8 <e, e>8 | % D 4
    <f, f>8 <af c' f'>8 <c, c>8 <af c' f'>8 | % D 5
    <f, f>8 <ef, ef>8 <c, c>8 <a, a>8 | % D 6
    <bf, bf>8 <af bf d'>8 <f, f>8 <af bf d'>8 | % D 7
    <bf,, bf,>8 <af bf d'>8 <bf,, bf,>8 r8 | % D 8
    <af, af>8 <af c' ef'>8 <ef, ef>8 <af c' ef'>8 | % D 9
    <a, a>8 <gf c' ef'>8 <ef, ef>8 <gf c' ef'>8 | % D 10
    <bf,, bf,>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % D 11
    <c, c>8 <g bf e'>8 <g, g>8 <e, e>8 | % D 12
    <f, f>8 <a c' ef'>8 <c, c>8 <a c' ef'>8 | % D 13
    <bf,, bf,>8 <af bf d'>8 <f, f>8 <d, d>8 | % D 14
    <ef, ef>8 <g bf ef'>8 <bf, bf>8 <g bf ef'>8 | % D 15
    <ef, ef>8 <bf,, bf,>8 <ef,, ef,>4\fermata | % D 16
  }
  \bar "|."
}

\score {
  \new PianoStaff <<
    \new Staff = "up" \upper
    \new Staff = "down" \lower
  >>
  \layout { }
}

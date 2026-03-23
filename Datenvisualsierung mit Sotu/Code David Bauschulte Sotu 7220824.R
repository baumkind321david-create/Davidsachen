install.packages(c("tidyverse", "tidytext", "ggwordcloud", "textclean", "widyr"))

library(tidyverse)
library(tidytext)
library(ggwordcloud)
library(textclean)

#https://cran.r-project.org/web/packages/widyr/widyr.pdf
library(widyr) #wegen Cosinusmatrix
#https://rdrr.io/cran/widyr/man/pairwise_similarity.html
library(dplyr)
library(igraph)
library(ggraph)
sotu <- read.csv2("C:\\Users\\baumk\\Downloads\\sotu_presidential_speeches.csv")

#bereinigung
tokens_bereinigungReden <- sotu %>% 
  mutate(speech = tolower(speech)) %>% 
  mutate(speech = replace_number(speech, remove = TRUE)) %>% 
  mutate(speech = replace_date(speech, replacement = "")) %>% 
  mutate(speech = replace_tag(speech)) %>% 
  mutate(speech = replace_url(speech)) %>% 
  mutate(speech = str_replace_all(speech, "\\d+", "")) %>% 
  unnest_tokens(word, speech) %>% 
  anti_join(stop_words, by = "word") %>%
  filter(nchar(word) > 2)%>%
  mutate(word_count = str_count(word, "\\S+")) %>% # zählt jedes Zeichen ohne Trennzeichen
  filter(!is.na(word_count))

word_counts <- tokens_bereinigungReden  %>%
  count(word, sort = TRUE) %>%
  slice_max(n, n = 100)

#1
presidents_to_compare <- c(
  "Abraham Lincoln",
  "Franklin D. Roosevelt",
  "John F. Kennedy",
  "Donald Trump"
)
last_9_presidents <- c(
  "Barack Obama",
  "George W. Bush",
  "Bill Clinton",
  "George H. W. Bush",
  "Ronald Reagan",
  "Jimmy Carter",
  "Gerald Ford",
  "Richard Nixon"
)

# Alle in einem Vektor vereinen (ohne Duplikate)
apresident_to_compare <- union(presidents_to_compare, last_9_presidents)

sotu_tf_idf <- tokens_bereinigungReden %>%
  filter(president %in% presidents_to_compare) %>%
  count(president, word, sort = TRUE) %>%
  bind_tf_idf(word, president, n)

#wegen Farbblindheit
okabe_ito <- c(
  "#E69F00", "#56B4E9", "#009E73", "#F0E442", 
  "#0072B2", "#D55E00", "#CC79A7", "#000000"
)

#https://dplyr.tidyverse.org/reference/top_n.html
sotu_tf_idf %>%
  group_by(president) %>%
  slice_max(tf_idf, n = 10) %>%
  ungroup() %>%
  #reorder wegen für jede einzelne Gruppe
  ggplot(aes(tf_idf, reorder_within(word, tf_idf, president), fill = president)) +
  geom_col(show.legend = FALSE) +
  #haben Sie mir geholfen mit y reorderer!!!!
  scale_y_reordered() + 
  facet_wrap(~president, scale = "free") +
  scale_fill_manual(values = okabe_ito) +theme_minimal() +
  labs(
    title = "Einzigartige Wörter pro Präsident (TF-IDF)",
    x = "Wichtigkeit (TF-IDF Score)", y = NULL
  )
ggsave("erstes.jpg", plot = last_plot(), width = 12, height = 8, dpi = 300)
#2
sotu_length <- tokens_bereinigungReden %>%
  mutate(word_count = str_count(word, "\\S+")) %>% # Zählt Gruppen von Nicht-Leerzeichen
  filter(!is.na(word_count)) #entferne wo NA
top_speeches <- sotu_length%>%
  slice_max(word_count, n = 10) #nimm nur die 10

#sortiert nach den Präsidenten mit der Wortanzahl!
ggplot(top_speeches, aes(x = reorder(paste(president, year), word_count), 
                         y = word_count, fill = party)) +
  geom_col() +
  coord_flip() +
  scale_fill_manual(values = c("Democratic" = "blue", "Republican" = "red", "Whig" = "orange")) +
  theme_minimal() + 
  geom_text(aes(label= word_count), position = position_stack(vjust = 0.9), col="white") +
  labs(title = "Die 10 längsten SOTU-Reden", subtitle = "von den amerikanischen Präsidenten",
       x = "Präsident & Jahr", y = "Anzahl der Wörter")
ggsave("zweites.jpg", plot = last_plot(), width = 12, height = 8, dpi = 300)
#3
ggplot(sotu_length, aes(x = year, y = word_count)) +
  # Jitter mit Mapping auf die Spalte 'sotu_type'
  geom_jitter(aes(color = sotu_type),
              width = 0.5,    
              height = 0,     
              size = 2,       
              alpha = 0.5) +  
  
  # Barrierefreie Farben: Türkis und ein rötliches Magenta
  scale_color_manual(values = c(
    "speech" = "#009E73",   # Ein sicheres Grün-Blau
    "written" = "#CC79A7"   # Ein sicheres rötliches Pink
  )) +
  #keine Schattierung wegen se bei geom_smoth
  geom_smooth(method = "loess", color = "black", se=FALSE) + 
  theme_light(base_size = 13) +
  theme(legend.position = "bottom") + 
  labs(
    title = "Entwicklung der Redelänge (1790 - heute)",
    subtitle = "Punkte zeigen einzelne Reden, die Linie den historischen Trend",
    x = "Jahr", 
    y = "Anzahl Wörter", 
    color = "Art der Rede"
  )
ggsave("drittes.jpg", plot = last_plot(), width = 12, height = 8, dpi = 300)
#3.1
# Wortanzahl pro Rede berechnen
speech_length <- tokens_bereinigungReden %>%
  group_by(president, year) %>%
  summarise(word_count = n()) %>% #wie viele Zeilen mit n()
  mutate(decade = floor(year / 10) * 10) # Gruppierung nach Jahrzehnten

#von PK2 mit den facotren, weil jede jahrzehnt als Kategorie
ggplot(speech_length, aes(x = as.factor(decade), y = word_count)) +
  geom_boxplot(fill = "#D55E00", alpha = 0.7) +
  geom_jitter(width = 0.2, alpha = 0.4) + # Zeigt die einzelnen Reden als Punkte
   #gleiche Skala zu erwingen
  scale_y_continuous(limits = c(0, 30000))+
  theme_minimal() +
  labs(title = "Entwicklung der Redenlänge (SOTU)",
       x = "Jahrzehnt", y = "Anzahl der Wörter (bereinigt)")
ggsave("viertes.jpg", plot = last_plot(), width = 12, height = 8, dpi = 300)
#3.2
# Wortlänge (wichtig recherche im Internet!!!!) und mit Ifelse in PK2
komplexitaet <- tokens_bereinigungReden %>%
  mutate(
    era = ifelse(
      year < 1900,
      "19. Jahrhundert",
      ifelse(
        year < 2000,
        "20. Jahrhundert",
        "21. Jahrhundert"
      )
    ),
    buchstaben = nchar(word)
  )
#nchar bei geekforgeeks (Anzahl der Zeichen)
#https://www.geeksforgeeks.org/sql/difference-between-char-and-nchar-ms-sql-server-datatypes/


#für Farbblinde und andere farben aus set1
era_colors <- c(
  "19. Jahrhundert" = "#7CAE00",
  "20. Jahrhundert" = "#00BFC4",
  "21. Jahrhundert" = "#C77CFF"
)

# Ausreißer weg https://statologie.de/ausreisser-entfernen-boxplots-r/
ggplot(komplexitaet, aes(x = era, y = buchstaben, fill = era)) +
  geom_boxplot(outlier.shape = NA) +
  coord_cartesian(ylim = c(0, 15)) +
  scale_fill_manual(values = era_colors) +
  theme_minimal() +
  labs(
    title = "Sprachliche Komplexität im Wandel",
    subtitle = "Durchschnittliche Wortlänge (Buchstaben) pro Ära",
    x = "Epoche",
    y = "Buchstaben pro Wort"
  )
ggsave("fünftes.jpg", plot = last_plot(), width = 12, height = 8, dpi = 300)
#4
library(ggplot2)
library(dplyr)
library(ggwordcloud)
library(maps)

# USA-Daten
usa <- map_data("state")

# Mittlere Koordinaten der Bundesstaaten
state_centers <- usa %>%
  group_by(region) %>%
  summarise(long = mean(range(long)),
            lat = mean(range(lat)))

# Top 50 Wörter WICHTIG KANN ANDERS AUSSEHEN WEGEN ZUFÄLIIG VERTEILUNG 
#mit den Wörtern
set.seed(123)
top_words <- word_counts %>% slice_max(n, n = 50)

# Wörter zufällig auf Bundesstaaten verteilen
word_states <- top_words %>%
  #wir wollen 50 zeilen mit zurüvklegen, also man kann mehrmals
  mutate(state = sample(state_centers$region, n(), replace = TRUE)) %>%
  left_join(state_centers, by = c("state" = "region"))
#mit left join jedes Wort verbnunden auch wenn kein NA

ggplot(usa, aes(x = long, y = lat, group= group)) +
  geom_polygon(fill = "grey95", color = "white", linewidth = 0.2) +
  geom_text_wordcloud(
    data = word_states,
    aes(label = word, size = n, color = n, x = long, y = lat), 
    inherit.aes = FALSE, #sonst verschiebt alles!
    #und anderer Datensatz nicht globale aes
    show.legend=TRUE
  ) +
  scale_size_area(max_size = 10) +
  scale_color_gradient(low = "darkblue", high = "red") + 
  theme_void()+ #koordinaten weg  
  labs(
    title = "SOTU Wordcloud",                      
    subtitle = "Häufigkeitsverteilung der Wörter in den State-of-the-Union-Reden",
    color = "Anzahl (n)",
    size = "Anzahl (n)"
  )
ggsave("sechstes.jpg", plot = last_plot(), width = 12, height = 8, dpi = 300)
#5
nrc_shares <- tokens_bereinigungReden %>%
  filter(president %in% apresident_to_compare) %>%  # nur gewünschte Präsidenten
  left_join(get_sentiments("nrc"), by = "word") %>%  # left_join, damit keiner verschwindet
  filter(!sentiment %in% c("positive", "negative"), !is.na(sentiment)) %>% #ich möchte NA weg
  #und positve und negative weg
  count(president, sentiment) %>%
  group_by(president) %>%
  mutate(percent = n / sum(n)) %>% #anteil berechnen
  ungroup()
okabe_ito_qual <- c(
  "#999999",  # Schwarz
  "#E69F00",  # Orange
  "#56B4E9",  # Himmelblau
  "#F0E442",  # Gelb
  "#0072B2",  # Blau
  "#D55E00",  # Rötlich
  "#009E73",  # Grün-Blau
  "#CC79A7"   # Pink
)
ggplot(nrc_shares, aes(x = president, y = percent, fill = sentiment)) +
  geom_col() +
  geom_text(aes(label = paste(round(percent * 100, 0), "%")),  # in % umwandeln und auf 0 runden
            position = position_stack(vjust = 0.5),
            color = "black",
            size = 3) +
  scale_fill_manual(values = okabe_ito_qual)+
  coord_flip() +
  theme_minimal() +
  labs(title = "Emotionale Zusammensetzung der Reden",
       x = "Präsident", y = "Anteil der Emotion", fill = "Emotion")
ggsave("siebtes.jpg", plot = last_plot(), width = 12, height = 8, dpi = 300)

#6
#eigene Kategorien:
economy_words <- c("jobs", "economy", "tax", "budget", "trade", "growth", "business", "inflation")
security_words <- c("war", "military", "defense", "security", "terror", "peace", "army", "border")
social_words <- c("health", "education", "school", "poverty", "families", "care", "welfare")
relig_words <- c("god", "bless", "faith", "prayer", "creator", "church")
saeulen_data_labels <- tokens_bereinigungReden %>%
  filter(party %in% c("Democratic", "Republican")) %>%
  mutate(
    Thema = ifelse(word %in% economy_words, "Wirtschaft",
                   ifelse(word %in% security_words, "Sicherheit",
                          ifelse(word %in% social_words, "Soziales",
                                 ifelse(word %in% relig_words, "Religion", NA))))
  ) %>%
  filter(!is.na(Thema)) %>%  # Wörter, die keiner Kategorie zugeordnet werden, raus
  count(party, Thema) %>%
  group_by(party) %>%
  mutate(percent = round((n / sum(n)) * 100, 1)) %>%
  ungroup()


#balken gestapelt durch fill
ggplot(saeulen_data_labels, aes(x = party, y = percent, fill = Thema)) +
  geom_col(position = "fill", color = "white") +
  geom_text(aes(label = paste(percent, "%")), 
            position = position_fill(vjust = 0.5), 
            color = "white", 
            fontface = "bold") +
  scale_fill_manual(values = okabe_ito_qual) +  # ← hier die neue Palette
  theme_minimal() + labs(y="relativer Anteil", title="Themen in den Sotureden")
ggsave("achtes.jpg", plot = last_plot(), width = 12, height = 8, dpi = 300)
#7

# 2. Wortfrequenzen pro Präsident berechnen
word_counts_matrix <- tokens_bereinigungReden %>%
  filter(president %in% apresident_to_compare) %>%
  count(president, word)
#wie ich da gekommen bin: Internet gesucht Ähnlichkeit der Wörter
#Kosinusmatrix mit paaren und widyr paket:
#https://cran.r-project.org/web/packages/widyr/widyr.pdf

#https://rdrr.io/cran/widyr/man/pairwise_similarity.html
similarity_matrix <- word_counts_matrix %>%
  pairwise_similarity(president, word, n)


ggplot(similarity_matrix, aes(x = item1, y = item2, fill = similarity)) +
  geom_tile(color = "white", linewidth = 0.2) + #heatmap
  
  # Magma Palette
  scale_fill_viridis_c(option = "magma", direction = -1) +
  
  geom_text(aes(label = round(similarity, 2)), 
            color = "white", 
            size = 3.5, 
            fontface = "bold") +
  
  theme_minimal() +
  labs(
    title = "Rhetorisches Echo: Wer klingt wie wer?",
    subtitle = "Cosine Similarity",
    x = NULL, y = NULL, fill = "Score"
  ) +
  theme( #aufgrund der Überlappung in x achse
    axis.text.x = element_text(angle = 45, hjust = 1, size = 10)
  )
ggsave("neuntes.jpg", plot = last_plot(), width = 12, height = 8, dpi = 300)
#8
target_president <- "Donald Trump"
top_20_data <- tokens_bereinigungReden %>%
  filter(president == target_president) %>%
  group_by(year) %>% #über jahre hinweg
  mutate(word2 = lead(word)) %>% #das nächste Wort https://dplyr.tidyverse.org/reference/lead-lag.html
  ungroup() %>%
  filter(!is.na(word2)) %>%
  count(word, word2, sort = TRUE) %>%
  slice_max(n, n = 20) 

# 2. In ungerichteten Graph umwandeln
bigram_graph <- graph_from_data_frame(top_20_data, directed = FALSE)



# 3. Plotting
set.seed(123)
ggraph(bigram_graph, layout = "fr") +
  geom_edge_link(aes(edge_width = n, edge_alpha = n), color = "#2c3e50", show.legend = TRUE) +
  scale_edge_width(name="Häufigkeit",range = c(1.5, 6)) + #dicke der kantwe
  scale_edge_alpha(name = "Häufigkeit") + #doppelter Namen
  geom_node_point(color = "#b22234", size = 8) +
  geom_node_text(aes(label = name), repel = TRUE, size = 5, fontface = "bold") + #text verschoeben wegen überlappungen
  theme_void() +
  labs(title = paste("Rhetorischer Kern:", target_president),
       subtitle = "Top 20 Wort-Assoziationen")
ggsave("41.jpg", plot = last_plot(), width = 12, height = 8, dpi = 300)
#9 postive und negative:
tokens_lastneu <- tokens_bereinigungReden %>%
  filter(president %in% apresident_to_compare)

tokens_sentiment <- tokens_lastneu%>%
  inner_join(get_sentiments("bing"), by = "word") #aus dem Lexikon bing

d <- tokens_sentiment %>%
  group_by(president, sentiment) %>%
  summarise(count = n()) %>%
  ungroup() %>%
  pivot_wider(names_from = sentiment, values_from = count) #jede Ausprgung in eine Spalte

sentiment_count <- d %>%
  mutate(score = positive - negative)  # negativer Score = eher negativ

ggplot(sentiment_count, aes(x = reorder(president, score), y = score, fill = score)) +
  geom_col() +
  geom_text(aes(label = score),
            position = position_stack(vjust = 0.5),
            color = "white", size = 4) +
  coord_flip() +
  scale_fill_gradient(
    low = "darkblue",  # niedrige Scores = dunkelblau
    high = "red",      # hohe Scores = rot
    name = "Score"
  ) +
  theme_minimal(base_size = 14) +
  labs(
    title = "Sentiment Score der Präsidenten",
    subtitle = "Score = Positive Wörter – Negative Wörter",
    x = "Präsident",
    y = "Sentiment Score"
  )
ggsave("elftes.jpg", plot = last_plot(), width = 12, height = 8, dpi = 300)
#9
party_tfidf <- tokens_bereinigungReden %>%
  filter(party %in% c("Democratic", "Republican")) %>%
  count(party, word) %>%
  bind_tf_idf(word, party, n) %>%
  group_by(party) %>%
  slice_max(tf_idf, n = 10) %>%
  ungroup()

#um Demokraten das negative zu zeigen von denen
party_tfidf %>%
  filter(party == "Democratic") %>%
  mutate(tf_idf = -tf_idf)
# 3. Visualisierung
ggplot(plot_data, aes(x = reorder(word, display_tfidf), y = display_tfidf, fill = party)) +
  geom_col() +
  coord_flip() +
  scale_fill_manual(values = c("Democratic" = "blue", "Republican" = "red")) +
  # Skala anpassen, damit keine negativen Zahlen an der Achse stehen
  scale_y_continuous(labels = abs) + 
  theme_minimal() +
  labs(
    title = "Politisches Profil: Demokraten vs. Republikaner",
    subtitle = "Links: Spezifisch für Demokraten | Rechts: Spezifisch für Republikaner (TF-IDF)",
    x = "Charakteristische Wörter",
    y = "Relevanz (TF-IDF Score)",
    fill = "Partei"
  ) 

ggsave("zwölftes.jpg", plot = last_plot(), width = 12, height = 8, dpi = 300)
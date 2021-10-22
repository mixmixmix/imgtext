fishes <- read.csv("input/finresoct.csv")
str(fishes)

plot(fishes$tsec,fishes$abs10)
modelnaive <- glm(fishes$abs10 ~ 1)
summary(modelnaive)

modelnaive <- glm(fishes$abs10 ~ 1)
summary(modelnaive)

modelflowstrenght <- glm(abs10 ~ fs*fishtype,fishes, family='gaussian')
summary(modelflowstrenght)

boxplot(fishes$fdist ~ fishes$fs)

boxplot(fishes$tsec ~ fishes$fs)

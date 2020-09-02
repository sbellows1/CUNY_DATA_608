library(ggplot2)
library(shiny)
library(dplyr)

df <- read.csv('data/cleaned-cdc-mortality-1999-2010-2.csv')

ui <- fluidPage(
  
  # Application title
  titlePanel("Mortality Across States"),
  
  # Sidebar with a slider input for number of bins
  sidebarLayout(
    sidebarPanel(
      selectInput("cause_of_death",
                  "Cause of Death",
                  unique(df$ICD.Chapter)),
      selectInput('states',
                  'States',
                  unique(df$State), multiple = T)
    ),
    
    # Show a plot of the generated distribution
    mainPanel(
      plotOutput("barPlot"),
      plotOutput("linePlot")
    )
  )
)

server <- function(input, output) {
  
  output$barPlot <- renderPlot({
    
    partial_df <- df %>% filter(Year == 2010) %>% filter(ICD.Chapter == input$cause_of_death)
    
    g <- partial_df %>% ggplot(aes(x = reorder(State, Crude.Rate), y = Crude.Rate)) + 
      geom_bar(stat = 'identity') + xlab('State') + 
      ylab('Mortality Rate') + ggtitle(paste('Mortality Rate by State for', as.character(input$cause_of_death), 'in 2010')) + theme(axis.text.x = element_text(angle = 90))
    print(g)
  })
  
  output$linePlot <- renderPlot({
    
    partial_df <- df %>% filter(ICD.Chapter == input$cause_of_death)
    nat_avg <- partial_df %>% group_by(Year) %>% group_map(function(x, ...){sum(x$Deaths)/sum(x$Population)*100000})
    nat_df <- data.frame('Year' = unique(partial_df$Year), 'Crude.Rate' = unlist(nat_avg), 'State' = rep('National Average', 12))
    state_df <- partial_df %>% filter(State %in% input$states) %>% select(c('Year', 'Crude.Rate', 'State'))
    full_df <- rbind(state_df, nat_df)
    
    g <- full_df %>% ggplot(aes(x = Year, y = Crude.Rate, col = State)) + geom_line() + geom_point() + ylab('Mortality Rate') + ggtitle(paste('Death Rate by', input$cause_of_death, 'vs. the National Average'))
    print(g)
    
  })
}

shinyApp(ui, server)
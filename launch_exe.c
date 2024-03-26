void execute_pipeline_redirection(t_data *data, t_Token *list_token, char **envp) 
{
    int index_fork;
    int input_fd;
    t_Token *curr;

    data->last = data->nb_cmd;
    curr = list_token;
    input_fd = STDIN_FILENO;
    data->first = 0;
    index_fork = 0;
    pid_t pid[data->last];
    

    while (curr != NULL) 
    {   
        if ((curr->type == E_WORD && curr->next != NULL) && (curr->next->Token_str[0] == '>') && (curr->next->next->type == E_FILE))   
        {
            pid[index_fork] = -1;        
            pid[index_fork] = fork_process_redi(data, curr, envp, list_token);
            index_fork++;
        }
        if (((curr->type == E_WORD || curr->next->type ==  E_FILE ) && curr->next != NULL && curr->next->Token_str[0] == '|') && (curr->type == E_WORD && curr->next == NULL))
        {        
            pid[index_fork] = -1;        
            create_pipe(data->pipe_fd, index_fork, data->last);
            pid[index_fork] = fork_process_pipe(index_fork, input_fd, data, curr, envp, list_token);
            close_pipes_in_parent(index_fork, data, &input_fd);
            index_fork++;

        }
        curr = curr->next;
    }
    wait_for_children(data->last, pid);
}

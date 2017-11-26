import React from 'react'
import { graphql } from 'react-apollo';
import gql from 'graphql-tag';

const query = gql`
query DetailView($id: ID!) {
  message(id: $id) {
    id,
    creationDate,
    message
  }
}
`

class DetailView extends React.Component {
  render() {
    let { data } = this.props
    if (data.loading || !data.message) {
      return (<div>Loading...</div>)
    }
    return (
      <div>
        <h1>Message {data.message.id}</h1>
        <p>{data.message.creationDate}</p>
        <p>{data.message.message}</p>
      </div>
    )
  }
}

// const queryOptions = {
//   options: { variables: { id: props.match.params.id } },
// }
const queryOptions = {
  options: props => ({
    variables: {
      id: props.match.params.id
    }
  })
}

DetailView = graphql(query, queryOptions)(DetailView)
export default DetailView
